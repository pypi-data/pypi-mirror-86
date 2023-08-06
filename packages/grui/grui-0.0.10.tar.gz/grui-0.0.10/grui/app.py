import inspect
import json
import os
import docstring_parser

from functools import wraps
from typing import *
from types import ModuleType
from enum import Enum
from dotenv import dotenv_values
from case_convert import upper_case
from flask import Flask, request, Response, send_file, send_from_directory, redirect, url_for
from flask_cors import CORS

from .decorator import GruiFunction
from .service import GruiService
from .typing import GruiModel, IncorrectDataWhileEncodingError
from .utils import convert_argument, GruiJsonEncoder, is_strong_password


##########
# Errors #
##########

class InvalidConfigError(RuntimeError):
    pass


#############
# Functions #
#############


def _find_argument(func: GruiFunction, path_parameters: Dict[str, str], body_parameters: Any) -> Dict[str, Any]:
    parameters_found = {}
    signature = inspect.signature(func.callable)

    annotations = dict(signature.parameters.items())
    if func.is_method:
        del annotations["self"]

    if len(annotations) == 0:
        yield {}

    nb_parameter = None

    for param_name in annotations:
        if param_name in path_parameters:
            tmp = convert_argument(annotations[param_name].annotation, path_parameters[param_name], func.multiple_action)
            if nb_parameter is not None and len(tmp) != nb_parameter:
                raise ValueError
            else:
                nb_parameter = len(tmp)
            parameters_found[param_name] = tmp

    if len(parameters_found.keys()) != len(annotations) and body_parameters is not None:
        missing_parameters = [x for x in annotations.keys() if x not in parameters_found.keys()]
        if len(missing_parameters) == 1:
            # Auto convert the body parameter to the missing param
            tmp = convert_argument(annotations[missing_parameters[0]].annotation, body_parameters, func.multiple_action)
            if nb_parameter is not None and len(tmp) != nb_parameter:
                raise ValueError
            else:
                nb_parameter = len(tmp)
            parameters_found[missing_parameters[0]] = tmp

    result = {}
    if func.multiple_action:
        for index in range(nb_parameter):
            for key in parameters_found:
                result[key] = parameters_found[key][index]
            yield result
    else:
        yield parameters_found


def _build4flask(func: GruiFunction):
    @wraps(func)
    def __inner(*args, **kwargs):
        try:
            code = func.default_return_code
            result = []
            for method_arguments in _find_argument(func, kwargs, request.json):
                for previous_action in func.previous_actions:
                    previous_action(code)
                res = func(*args, **method_arguments)
                for next_action in func.next_actions:
                    (res, code) = next_action(res, code)
                if res is None:
                    return Response(json.dumps(res, cls=GruiJsonEncoder), status=code, content_type="application/json")
                if func.multiple_action:
                    result.append(res)
                else:
                    return Response(json.dumps(res, cls=GruiJsonEncoder), status=code, content_type="application/json")
            return Response(json.dumps(result, cls=GruiJsonEncoder), status=code, content_type="application/json")
        except IncorrectDataWhileEncodingError as e:
            return Response(json.dumps(str(e), cls=GruiJsonEncoder), status=400, content_type="application/json")
    return __inner


###########
# Classes #
###########

class LogLevel(Enum):
    """
    Define the log level. Useful to sort the message printed.
    """
    NONE = 0
    WARN = 1
    INFO = 2
    ALL = 3


class GruiApp:

    def __init__(self, title: str = None, service_package: ModuleType = None):
        from .service import GruiDocService
        self.__flask_app = None
        self.__config = {}
        self.load_config()
        self.title = title if title is not None else os.path.split(os.getcwd())[-1]
        self.registered_service = {}
        self.registered_function = {}
        self.registered_type = {}
        self.service_doc = {}
        self.register_service(GruiDocService)
        if service_package is not None:
            self.register_package(service_package)

    @property
    def built(self) -> bool:
        return self.__flask_app is not None

    @property
    def config(self) -> Dict[str, Any]:
        if self.built:
            return self.__flask_app.config
        else:
            return self.__config

    def register_package(self, package: ModuleType):
        """
        This function will look at every member of the module.
        If some are subclass of 'GruiService'. They'll be be added to application.
        """
        for name, member in inspect.getmembers(package, lambda c: inspect.isclass(c) and issubclass(c, GruiService)):
            self.register_service(member)

    def register_service(self, service_class: Type[GruiService]):
        """
        Register every decorated function from the service class.
        """
        if self.registered_service.get(service_class) is not None:
            return

        service_init_arguments = []
        signature = inspect.signature(service_class.__init__)
        for name, parameter in signature.parameters.items():
            if isinstance(self, parameter.annotation):
                service_init_arguments.append(self)
            elif issubclass(parameter.annotation, GruiService):
                self.register_service(parameter.annotation)
                service_init_arguments.append(self.registered_service[parameter.annotation])
        service_instance = service_class(*service_init_arguments)
        self.registered_service[service_class] = service_instance

    def register_function(self, function: GruiFunction):
        """
        Register the function to the application.
        """
        self.registered_function[function.id] = function
        if function.result is not None:
            function.result.type.register(self.registered_type)
        for argument in function.args.values():
            argument.type.register(self.registered_type)
        for service_class in self.registered_service.keys():
            if self.service_doc.get(service_class.url_prefix) is not None and \
                    function.path.startswith(self.config["URL_PREFIX"] + service_class.url_prefix):
                self.service_doc[service_class.url_prefix].methods.append(function)

    def build_wsgi(self, import_name: str, logger_override=None, **kwargs):
        from .service import GruiDocService

        if not self.built:
            self.__config.setdefault('ENVIRONMENT', "development")
            self.__config.setdefault('INDEX_FILE_PATH', os.path.join(os.path.dirname(os.getcwd()), "index.html"))
            self.__config.setdefault('STATIC_FOLDER_PATH', os.path.join(os.path.dirname(os.getcwd()), "static"))
            self.__config.setdefault('URL_PREFIX', "/api")

            if os.path.isdir(self.config['STATIC_FOLDER_PATH']):
                self.__flask_app = Flask(import_name,
                                         static_folder=self.config['STATIC_FOLDER_PATH'],
                                         static_url_path='/static',
                                         **kwargs)
            else:
                self.__flask_app = Flask(import_name, static_folder=None, **kwargs)
            self.__flask_app.config.update(self.__config)
            self.__flask_app.config['ENV'] = self.__config.get('ENVIRONMENT')
            self.__flask_app.config['FLASK_ENV'] = self.__config.get('ENVIRONMENT')

            self.log(LogLevel.INFO, "Starting application in", self.config['ENVIRONMENT'])

            if os.path.isfile(self.config['INDEX_FILE_PATH']):
                self.log(LogLevel.INFO, "Register index:", self.config['INDEX_FILE_PATH'])
                self.__flask_app.route('/')(self.serve_index_file)

            if os.path.isdir(self.config['STATIC_FOLDER_PATH']):
                self.log(LogLevel.INFO, "Register static folder:", self.config['STATIC_FOLDER_PATH'])
                self.__flask_app.route('/favicon')(GruiApp.serve_favicon_file)

            if self.config['URL_PREFIX'][-1] != '/':
                self.config['URL_PREFIX'] += "/"

            if not self.validate_config():
                raise InvalidConfigError(self.config)

            if logger_override is not None:
                self.__flask_app.logger.handlers = logger_override.handlers
                self.__flask_app.logger.setLevel(logger_override.level)

            # Register every decorated function into the flask application
            for service_class, service_instance in self.registered_service.items():
                if service_class != GruiDocService:
                    self.service_doc[service_class.url_prefix] = _GruiServiceDoc(service_class)
                for _, method in inspect.getmembers(service_instance, lambda m: isinstance(m, GruiFunction)):
                    self.register_function(method)

            CORS(self.__flask_app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "GRUI"]}})
            self.__flask_app.url_map.strict_slashes = False
            # self.__flask_app.route('/shutdown', methods=['GET'])(GruiApp.shutdown_server)

            for function in self.registered_function.values():
                self.log(LogLevel.INFO, "Register function:", "%-7s" % function.method, function.path)
                self.__flask_app.route(function.path, methods=[function.method])(_build4flask(function))

        return self.__flask_app

    def log(self, level: LogLevel, *args):
        log_level = level.name.lower()
        if log_level in dir(self.__flask_app.logger):
            getattr(self.__flask_app.logger, log_level)(" ".join(args))

    def run(self, **kwargs):
        if not self.built:
            self.build_wsgi('__main__')
        self.__flask_app.run(**kwargs)

    def load_config(self):
        env_file_path = os.getenv('GRUI_ENV_FILE', "./.env")
        for name, value in dotenv_values(env_file_path).items():
            self.__config[name] = value

    def validate_config(self) -> bool:
        if self.config['ENVIRONMENT'] == "production":
            secret_key = self.config.get("SECRET_KEY", None)
            return type(secret_key) == str and len(secret_key) >= 36 and is_strong_password(secret_key)
        return True

    @staticmethod
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def serve_index_file(self):
        print("serving index", self.config['INDEX_FILE_PATH'])
        return send_file(self.config['INDEX_FILE_PATH'])

    @staticmethod
    def serve_favicon_file():
        return redirect("/static/favicon.ico")


class _GruiServiceDoc(GruiModel):

    id: str
    name: str
    methods: List[GruiFunction]
    presentation: str
    description: str

    def __init__(self, service_class):
        doc_parsed = docstring_parser.parse(service_class.__doc__)
        super().__init__(id=service_class.url_prefix,
                         name=upper_case(service_class.__name__),
                         methods=[],
                         presentation=doc_parsed.short_description or "",
                         description=doc_parsed.long_description or "")

    def validate(self) -> bool:
        return True

import json
import re

from inspect import isclass
from typing import *

from .typing import GruiModel


def convert_argument_list(type_: type, value: Any) -> List[Any]:
    """
    Convert any value to a list.

    :param type_:  The type of the element contained into the list.
    :param value:  The value to convert to the right type.

    :return:  The list converted to the right type
    """

    # Initialize the result
    result = []
    # First wz check if we already have a list.
    if isinstance(value, (list, tuple)):
        for tmp in value:
            result.append(convert_argument(type_, tmp, False))
    # Maybe this is a list of value separated by comma
    elif isinstance(value, str):
        for tmp in value.split(","):
            result.append(convert_argument(type_, tmp, False))
    else:
        result.append(convert_argument(type_, value, False))
    return result


def convert_argument(type_: type, value: Any, to_list: bool) -> Any:
    if to_list:
        return convert_argument_list(type_, value)
    else:
        if type_ is int:
            return int(value)
        elif type_ is float:
            return float(value)
        elif type_ is bool:
            return bool(value)
        elif get_origin(type_) == list:
            return convert_argument_list(get_args(type_)[0], value)
        elif isclass(type_) and issubclass(type_, GruiModel):
            return type_.from_json(value)
    return value


def dict2list(dict_: dict) -> List[dict]:
    """:return A list of dict where every dict contains one value"""
    result = []
    for key in dict_:
        for i, value in enumerate(dict_[key]):
            try:
                result[i][key] = value
            except IndexError:
                result.append({key: value})
    return result


class GruiJsonEncoder(json.JSONEncoder):

    __DICT_VALUES_TYPE = type({}.values())
    __DICT_KEYS_TYPE = type({}.keys())

    def default(self, obj):
        from .typing import GruiJsonSerializable

        if isinstance(obj, GruiJsonEncoder.__DICT_VALUES_TYPE) or isinstance(obj, GruiJsonEncoder.__DICT_KEYS_TYPE):
            return tuple(obj)
        elif isinstance(obj, GruiJsonSerializable):
            return obj.to_json()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


_REGEX_HAVE_DIGIT = re.compile("\\d")
_REGEX_HAVE_UPPER = re.compile("[a-z]")
_REGEX_HAVE_LOWER = re.compile("[A-Z]")
_REGEX_HAVE_SYMBOL = re.compile("[!#:;$%&'()*+,\\]\\-/[^_`}{|~\"]")


def is_strong_password(password: str):
    # Check the length
    if len(password) < 8:
        return False
    # Search for at least one digit
    if _REGEX_HAVE_DIGIT.search(password) is None:
        return False
    # Search for at least one upper case
    if _REGEX_HAVE_UPPER.search(password) is None:
        return False
    # Search for at least one lower case
    if _REGEX_HAVE_LOWER.search(password) is None:
        return False
    # Search for at least one symbol
    if _REGEX_HAVE_SYMBOL.search(password) is None:
        return False
    return True

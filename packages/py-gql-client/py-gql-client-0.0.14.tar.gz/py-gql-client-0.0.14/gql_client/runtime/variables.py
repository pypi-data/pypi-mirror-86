#!/usr/bin/env python3

from typing import Any, Dict, Union

from dataclasses_json import DataClassJsonMixin
from datetime import datetime
from enum import Enum

from .datetime_utils import isoformat
from .enum_utils import MissingEnumException


def encode_value(
    value: Union[DataClassJsonMixin, datetime, Enum]
) -> Union[Dict[str, Any], str]:
    if isinstance(value, DataClassJsonMixin):
        return encode_variables(value.to_dict())
    elif isinstance(value, datetime):
        return isoformat(value)
    elif isinstance(value, Enum):
        if value.value == "":
            raise MissingEnumException(value)
        return value.value
    return value


def encode_variables(variables: Dict[str, Any]) -> Dict[str, Any]:
    new_variables: Dict[str, Any] = {}
    for key, value in variables.items():
        if (
            isinstance(value, DataClassJsonMixin)
            or isinstance(value, datetime)
            or isinstance(value, Enum)
        ):
            new_variables[key] = encode_value(value)
        elif isinstance(value, list):
            new_list = []
            for val in value:
                if (
                    isinstance(val, DataClassJsonMixin)
                    or isinstance(val, datetime)
                    or isinstance(val, Enum)
                ):
                    new_list.append(encode_value(val))
                else:
                    new_list.append(val)
            new_variables[key] = new_list
        else:
            new_variables[key] = value
    return new_variables

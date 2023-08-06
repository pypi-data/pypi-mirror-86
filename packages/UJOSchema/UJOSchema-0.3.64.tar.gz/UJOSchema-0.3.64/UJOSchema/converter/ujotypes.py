#
# Copyright (c) 2018-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" conversion of a schema into a an empty UjoType instance """

from datetime import datetime
from typing import Union, Sequence

from ujotypes import UjoMap, UJO_VARIANT_NONE, UjoList

from UJOSchema.schema import UjsSchema
from UJOSchema.types import UjsUtf8String, Typedef, UjsList, UjsMap, CustomType, Record, Object
from UJOSchema.converter.base import BaseSchemaConverter, BaseTypeConverter


UJO_EMPTY_DEFAULTS = {
    "bool": False,
    "int8": 0,
    "int16": 0,
    "int32": 0,
    "int64": 0,
    "uint8": 0,
    "uint16": 0,
    "uint32": 0,
    "uint64": 0,
    "float16": 0.0,
    "float32": 0.0,
    "float64": 0.0,
    "date": "nyi",
    "time": "nyi",
    "datetime": "nyi",
    "timestamp": datetime(2000, 1, 1),
    "string": "",
    "cstring": "",
    "binary": "nyi",  # bytes(),
    "variant": None,
}


def schema_to_type(schema: Union[str, UjsSchema], target: str):
    if isinstance(schema, str):
        schema = UjsSchema.from_str(schema)

    return SchemaToType(schema, target).convert()


class SchemaToType(BaseSchemaConverter):
    def __init__(self, schema, target):
        super().__init__(schema, target)

    def convert(self):
        return TypeToUjoTypeConverter(self.schema, self.schema[self.target]).convert()


class TypeToUjoTypeConverter(BaseTypeConverter):
    def convert(self):
        default_converter = BasicTypeToUjo
        converters = {
            CustomType: CustomTypeToUjo,
            UjsList: ContainerToUjo,
            UjsMap: ContainerToUjo,
            Record: RecordToUjo,
            Object: ObjectToUjo,
        }
        if isinstance(self.type, Typedef):
            converter = converters.get(type(self.type.type)) or default_converter
        else:
            converter = converters.get(type(self.type)) or default_converter

        return converter(self.schema, self.type).convert()


class BasicTypeToUjo(BaseTypeConverter):
    def convert(self):
        # TO_DO: consider: not null: default and constraints in / not in (range)

        default_type = self.type.type
        if isinstance(self.type.type, Sequence):
            default_type = self.type.type[0]

        default = UJO_EMPTY_DEFAULTS.get(default_type.name)
        return self.type.default_to_ujo(default)


class CustomTypeToUjo(BaseTypeConverter):
    def convert(self):
        return schema_to_type(self.schema, target=self.type.type.name)


class ContainerToUjo(BaseTypeConverter):
    def convert(self):
        return self.type.type.default_to_ujo()


class RecordToUjo(BaseTypeConverter):
    def convert(self):
        if self.type.extends:
            result_list = schema_to_type(self.schema, self.type.extends.name)
        else:
            result_list = UjoList()

        for item in self.type:
            value = TypeToUjoTypeConverter(self.schema, item).convert()
            result_list.append(value)
        return result_list


class ObjectToUjo(BaseTypeConverter):
    def convert(self):
        if self.type.extends:
            result_map = schema_to_type(self.schema, target=self.type.extends.name)
            self.type.type = self.schema[self.type.extends.name].type
        else:
            result_map = UjoMap()

        class Undefined:
            name = "undefined"
            default_to_ujo = lambda *args: UJO_VARIANT_NONE  # noqa

        try:
            key_types, value_types = self.type.type.type
        except (AttributeError, TypeError):
            # in case the definition was not explict // without <key -> value> definition
            key_types, value_types = UjsUtf8String, Undefined

        if not isinstance(key_types, Sequence):
            key_types = [key_types]

        for item in self.type.items:
            item_type = item.type or value_types
            if isinstance(item_type, Sequence):
                # let's simply take the first item to instantiate a value
                item_type = item_type[0]

            if isinstance(item.type, CustomType):
                value = schema_to_type(self.schema, target=item.type.name)
            else:
                default = UJO_EMPTY_DEFAULTS.get(item_type.name)
                value = item_type.default_to_ujo(default)

            for key_type in key_types:
                # try to find a matching key type for the field name
                try:
                    result_map[key_type.default_to_ujo(item.name)] = value
                except (TypeError, ValueError):
                    continue
                else:
                    break
            else:
                raise TypeError(f"No key type matching {item.name} (available: {key_types})")

        return result_map

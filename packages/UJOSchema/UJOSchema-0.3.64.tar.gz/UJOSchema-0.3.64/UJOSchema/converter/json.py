#
# Copyright (c) 2020-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#


""" serialization of a schema into JSON """

import json
from abc import ABC, abstractmethod

from UJOSchema.types import Module, Object, Record
from UJOSchema.constraints import UjsNotNull, UjsIn, UjsNotIn, UjsOfLength
from UJOSchema.ranges import UjsAbove, UjsBelow

from .base import BaseSchemaConverter, BaseTypeConverter


def schema_to_json(schema, target=None):
    return SchemaToJSON(schema).convert(target)


class SchemaToJSON(BaseSchemaConverter):
    def __init__(self, schema):
        super().__init__(schema)
        self.type_converter = TypeToJSONConverter(self.schema, None)
        self.convert_type = self.type_converter.convert_type

    def convert(self, target=None):  # pylint: disable=arguments-differ

        converted = [
            self.convert_type(typ)
            for typ in self.schema.values()
            if not isinstance(typ, Module)
        ]

        converted = merge_extends(converted)

        if target:
            converted = get_target(converted, target)

        return json.dumps(list(converted.values()), indent=4)


class TypeToJSONConverter(BaseTypeConverter):
    def __init__(self, schema, typ, optional=False):
        super().__init__(schema, typ)
        self.__elements = None
        self.optional = optional

    def convert(self):
        return self.convert_type(self.type)

    def convert_type(self, typ, optional=False):
        default_converter = BasicTypeToJSON
        converters = {Record: ContainerToJSON, Object: ContainerToJSON}

        converter = converters.get(type(typ)) or default_converter
        return converter(self.schema, typ, optional).convert()

    @property
    def name(self):
        return "" if not self.type else self.type.name

    @property
    def type_name(self):
        return ""

    @property
    def doc(self):
        return "" if not self.type else self.type.doc or ""

    @property
    def list_type(self):
        if self.type_name == "list":
            return self.type.type.type.name
        return None

    @property
    def key_value_types(self):
        if self.type_name == "map":
            return [typ.name for typ in self.type.type.type]
        return None

    @property
    def constraints(self):
        if self.type and hasattr(self.type, "constraint"):
            return get_constraints(self.type.constraint)
        return None

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, values):
        self.__elements = values

    def to_dict(self):
        json_elements = {"name": self.name, "type": self.type_name, "doc": self.doc}
        if self.constraints:
            json_elements["constraints"] = self.constraints
        if self.list_type:
            json_elements["list_type"] = self.list_type
        if self.key_value_types:
            json_elements["key_value_types"] = self.key_value_types
        if self.elements:
            json_elements["elements"] = self.elements
        if self.optional:
            json_elements["optional"] = self.optional
        return json_elements


class BasicTypeToJSON(TypeToJSONConverter):
    @property
    def type_name(self):
        if hasattr(self.type.type, "name"):
            return self.type.type.name

        return [typ.name for typ in self.type.type]

    def convert(self):
        return self.to_dict()


class ContainerToJSON(TypeToJSONConverter):
    @property
    def type_name(self):
        if getattr(self.type, "extends"):
            return "extends_" + self.type.extends.name

        if isinstance(self.type, Record):
            return "record"

        if isinstance(self.type, Object):
            return "object"
        return ""

    def convert(self):
        elem = []
        for item in self.type:
            optional = item.optional if hasattr(item, "optional") else False
            if not item.type:
                item.type = self.type.type.type[1]
            elem.append(self.convert_type(item, optional))

        self.elements = elem
        return self.to_dict()


def get_constraints(typ_constraints):
    if not typ_constraints:
        return None

    converters = {
        UjsNotNull: NotConstraintToJSON,
        UjsOfLength: LengthConstraintToJSON,
        UjsIn: InConstraintToJSON,
        UjsNotIn: NotConstraintToJSON,
    }
    constraints = []
    for constraint in typ_constraints:
        converter = converters.get(type(constraint))
        constraints.append(converter(constraint).convert())
    return constraints


class ConstraintToJSONConverter(ABC):
    def __init__(self, constraint):
        self.constraint = constraint

    @abstractmethod
    def convert(self):
        pass


class InConstraintToJSON(ConstraintToJSONConverter):
    def convert(self):
        def replace_symbols(val):
            val = val.__str__().replace("<=", "..")
            if ">=" in val:
                val = val.replace(">=", "") + ".."
            return val

        return {"in": [replace_symbols(con) for con in self.constraint.values]}


class LengthConstraintToJSON(ConstraintToJSONConverter):
    def convert(self):
        default_converter = LengthConverter
        converters = {UjsBelow: LengthBelowConverter, UjsAbove: LengthAboveConverter}
        converter = converters.get(type(self.constraint.length)) or default_converter
        return {"length": [converter(self.constraint).convert()]}


class LengthBelowConverter(ConstraintToJSONConverter):
    def convert(self):
        return str(self.constraint.length).replace("<=", "..")


class LengthAboveConverter(ConstraintToJSONConverter):
    def convert(self):
        return str(self.constraint.length).replace(">=", "") + ".."


class LengthConverter(ConstraintToJSONConverter):
    def convert(self):
        return str(self.constraint.length)


class NotConstraintToJSON(ConstraintToJSONConverter):
    def convert(self):
        converters = {UjsNotIn: NotInConverter, UjsNotNull: NotNullConverter}
        converter = converters.get(type(self.constraint))
        return {"not": converter(self.constraint).convert()}


class NotInConverter(ConstraintToJSONConverter):
    def convert(self):
        val = str(self.constraint).replace("not in", "")
        val = val.replace("<=", "..")
        if ">=" in val:
            val = val.replace(">=", "") + ".."
        return "in (" + val + " )"


class NotNullConverter(ConstraintToJSONConverter):
    def convert(self):
        return str(self.constraint).replace("not", "")


def merge_extends(type_list):
    """merge extended type definitions into their parent types"""
    extensions = {
        typ.get("type").replace("extends_", ""): typ
        for typ in type_list
        if "extends" in typ.get("type")
    }
    extended = {typ.get("name"): typ for typ in type_list}
    for type_name, typ in extensions.items():
        extended[typ.get("name")]["type"] = extended[type_name].get("type")
        extended[typ.get("name")]["elements"] = (
            extended[type_name].get("elements") + extended[typ.get("name")]["elements"]
        )
    return extended


def get_target(converted, target):
    """get only target type and its custom types"""
    target_types = {target: converted[target]}

    if isinstance(converted[target].get("type"), list):
        return target_types

    if converted[target].get("type") in converted:
        custom = get_target(converted, converted[target].get("type"))
        target_types.update(custom)

    if "elements" in converted[target]:
        for element in converted[target].get("elements"):
            if element.get("type") in converted:
                custom_element = get_target(converted, element.get("type"))
                target_types.update(custom_element)

    return target_types

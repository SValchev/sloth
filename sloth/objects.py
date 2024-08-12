from dataclasses import dataclass, field
import json
from typing import Protocol

from copy import deepcopy
from enum import StrEnum, unique

from sloth.ast import BlockStatement, Identifier


@unique
class Types(StrEnum):
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    FAULT = "FAULT"
    ENVIRONMENT = "ENVIRONMENT"
    FUNC = "FUNC"


class ObjectType(str):
    @classmethod
    def from_type(cls, str_: Types):
        return cls(str_)


class SlothObject(Protocol):
    def type(self) -> ObjectType: ...

    def inspect(self) -> str: ...


class Environment(SlothObject, dict):
    def copy(self):
        return deepcopy(self)

    def type(self) -> ObjectType:
        return ObjectType.from_type(Types.INTEGER)

    def inspect(self) -> str:
        return json.dumps(self, indent=4)


@dataclass(frozen=True, slots=True)
class Integer(SlothObject):
    value: int

    def type(self) -> ObjectType:
        return ObjectType.from_type(Types.INTEGER)

    def inspect(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class Boolean(SlothObject):
    value: bool

    def type(self) -> ObjectType:
        return ObjectType.from_type(Types.BOOLEAN)

    def inspect(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class Null(SlothObject):
    def type(self) -> ObjectType:
        return ObjectType.from_type(Types.NULL)

    def inspect(self) -> str:
        return "Null"


@dataclass(frozen=True, slots=True)
class Fault(SlothObject):
    message: str

    def type(self) -> ObjectType:
        return ObjectType.from_type(Types.FAULT)

    def inspect(self) -> str:
        return "Fault"


@dataclass(frozen=True, slots=True)
class Function(SlothObject):
    arguments: list[Identifier]
    body: BlockStatement
    env: Environment = field(default_factory=Environment)

    def type(self) -> ObjectType:
        return ObjectType.from_type(Types.FUNC)

    def inspect(self) -> str:
        args = ", ".join(map(str, self.arguments))
        return f"func({args}) {{ {str(self.body)} }}"

from dataclasses import dataclass, field
import json
from typing import Protocol, Any

from enum import StrEnum, unique


@unique
class Types(StrEnum):
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    FAULT = "FAULT"
    ENVIRONMENT = "ENVIRONMENT"


class ObjectType(str):
    @classmethod
    def from_type(cls, str_: Types):
        return cls(str_)


class SlothObject(Protocol):
    def type(self) -> ObjectType: ...

    def inspect(self) -> str: ...


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

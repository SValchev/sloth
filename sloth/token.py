from enum import StrEnum, auto
from dataclasses import dataclass


class TokenType(StrEnum):
    EOF = (auto(),)
    ILLEGAL = (auto(),)

    IDENT = (auto(),)
    INT = (auto(),)

    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"

    SEMICOLON = ";"
    COMMA = ","

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    VAR = "var"
    FUNC = "func"


@dataclass(frozen=True)
class Token:
    type: TokenType
    literal: str

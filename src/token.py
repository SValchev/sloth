from enum import StrEnum
from dataclasses import dataclass


class TokenType(StrEnum):
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"

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
    FUNCTION = "func"


@dataclass(frozen=True)
class Token:
    type: TokenType
    literal: str

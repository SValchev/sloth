from typing import Self
from enum import StrEnum, auto
from dataclasses import dataclass


class TokenType(StrEnum):
    EOF = auto()
    ILLEGAL = auto()

    IDENT = auto()
    INT = auto()

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


_keywords: dict[TokenType | str, TokenType] = {
    TokenType.FUNC: TokenType.FUNC,
    TokenType.VAR: TokenType.VAR,
}


@dataclass(frozen=True)
class Token:
    type: TokenType
    literal: str

    @classmethod
    def from_word(cls, word: str) -> "Token":
        token_type = _keywords.get(word, TokenType.IDENT)
        return Token(token_type, word)

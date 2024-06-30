from typing import Self
from enum import StrEnum, auto
from dataclasses import dataclass


class TokenType(StrEnum):
    """
    ==
    !=
    return
    if
    else
    true
    false
    >
    <
    !
    *
    /
    """

    EOF = auto()
    ILLEGAL = auto()

    IDENT = auto()
    INT = auto()

    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    GT = ">"
    LT = "<"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"

    SEMICOLON = ";"
    COMMA = ","

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    VAR = "var"
    FUNC = "func"

    RETURN = 'return'
    IF = "if"
    ELSE = "else"
    TRUE = "true"
    FALSE = "false" 

_keywords: dict[TokenType | str, TokenType] = {
    TokenType.FUNC: TokenType.FUNC,
    TokenType.VAR: TokenType.VAR,
    #TokenType.RETURN: TokenType.RETURN,
    #TokenType.IF: TokenType.IF,
    #TokenType.ELSE: TokenType.ELSE,
}


@dataclass(frozen=True)
class Token:
    type: TokenType
    literal: str

    @classmethod
    def from_word(cls, word: str) -> "Token":
        token_type = _keywords.get(word, TokenType.IDENT)
        return Token(token_type, word)

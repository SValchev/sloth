from dataclasses import dataclass, asdict
from enum import StrEnum, auto


class TokenType(StrEnum):
    EOF = "\00"
    ILLEGAL = ""

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

    STRING = "STRING"

    EQ = "=="
    NOT_EQ = "!="

    SEMICOLON = ";"
    COMMA = ","

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    VAR = "var"
    FUNC = "func"

    RETURN = "return"
    IF = "if"
    ELSE = "else"
    TRUE = "true"
    FALSE = "false"


_keywords: dict[TokenType | str, TokenType] = {
    TokenType.FUNC: TokenType.FUNC,
    TokenType.VAR: TokenType.VAR,
    TokenType.RETURN: TokenType.RETURN,
    TokenType.IF: TokenType.IF,
    TokenType.ELSE: TokenType.ELSE,
    TokenType.TRUE: TokenType.TRUE,
    TokenType.FALSE: TokenType.FALSE,
}


@dataclass(frozen=True)
class Token:
    type: TokenType
    literal: str

    @classmethod
    def from_word(cls, word: str) -> "Token":
        token_type = _keywords.get(word, TokenType.IDENT)
        return Token(token_type, word)

    def copy_self(self):
        return self.copy(self)

    @classmethod
    def copy(cls, other: "Token"):
        if not isinstance(other, cls):
            raise ValueError("Other is not type same type")
        return cls(**asdict(other))

from sloth.lexer import Lexer
from sloth.token import TokenType

from .helpers import validate_input


def test_init_token():
    input_ = "=+(){},;><!*/"

    expected = [
        (TokenType.ASSIGN, "="),
        (TokenType.PLUS, "+"),
        (TokenType.LPAREN, "("),
        (TokenType.RPAREN, ")"),
        (TokenType.LBRACE, "{"),
        (TokenType.RBRACE, "}"),
        (TokenType.COMMA, ","),
        (TokenType.SEMICOLON, ";"),
        (TokenType.GT, ">"),
        (TokenType.LT, "<"),
        (TokenType.BANG, "!"),
        (TokenType.ASTERISK, "*"),
        (TokenType.SLASH, "/"),
        (TokenType.EOF, ""),
    ]

    validate_input(input_, expected)

from sloth.lexer import Lexer
from sloth.token import TokenType


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

    lexer = Lexer(input_)

    for token_type, literal in expected:
        token = lexer.next_token()

        assert token.literal == literal
        assert token.type == token_type

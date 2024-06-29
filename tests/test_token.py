from src.lexer import Lexer
from src.token import TokenType


def test_init_token():
    input_ = "=+(){},;"

    expected = [
        (TokenType.ASSIGN, "="),
        (TokenType.PLUS, "+"),
        (TokenType.LPAREN, "("),
        (TokenType.RPAREN, ")"),
        (TokenType.LBRACE, "{"),
        (TokenType.RBRACE, "}"),
        (TokenType.COMMA, ","),
        (TokenType.SEMICOLON, ";"),
    ]

    lexer = Lexer(input_)

    for token_type, literal in expected:
        token = lexer.next_token()

        assert token.literal == literal
        assert token.type == token_type

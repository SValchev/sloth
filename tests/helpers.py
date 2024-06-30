from sloth.lexer import Lexer
from sloth.token import TokenType

_expected_type = list[tuple[TokenType, str]]


def validate_input(input_: str, expected: _expected_type) -> None:
    lexer = Lexer(input_)
    for token_type, literal in expected:
        token = lexer.next_token()

        assert token.literal == literal
        assert token.type == token_type

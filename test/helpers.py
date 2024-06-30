from typing import Tuple

from sloth.lexer import Lexer
from sloth.token import TokenType


def validate_input(input_: str, expected: Tuple[TokenType, str]) -> None:
    lexer = Lexer(input_)
    for token_type, literal in expected:
        token = lexer.next_token()

        assert token.literal == literal
        assert token.type == token_type

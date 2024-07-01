from sloth.ast import Program
from .lexer import Lexer


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer: Lexer = lexer

    @classmethod
    def from_input(cls, input_: str) -> "Parser":
        lexer = Lexer(input_)
        return cls(lexer)

    def parse_program(self) -> Program:
        return Program()

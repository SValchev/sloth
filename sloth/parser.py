from typing import Optional
from .token import Token, TokenType
from .ast import Identifier, Program, ReturnStatement, VarStatement
from .lexer import Lexer


class ParsingError:
    def __init__(self, message: str) -> None:
        self.message = message


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.errors: list[ParsingError] = []
        self._lexer: Lexer = lexer

        self._token: Token
        self._peek_token: Token
        self._next_token()
        self._next_token()

    @classmethod
    def from_input(cls, input_: str) -> "Parser":
        lexer = Lexer(input_)
        return cls(lexer)

    def parse_program(self) -> Program:
        program = Program()

        while not self._token_is(TokenType.EOF):
            statement = self._parse_statement()
            if statement:
                program.add_statement(statement)
            self._next_token()

        return program

    def _parse_statement(self):
        match self._token.type:
            case TokenType.VAR:
                return self._parse_var_stmt()
            case TokenType.RETURN:
                return self._parse_return_stmt()
        return None

    def _next_token(self) -> Token:
        self._token = self._peek_token
        self._peek_token = self._lexer.next_token()
        return self._token

    def _parse_return_stmt(self) -> ReturnStatement:
        result = ReturnStatement(self._token, None)

        # Loop until the end of the expression
        while self._token_is(TokenType.SEMICOLON):
            self._next_token()

        return result

    def _parse_var_stmt(self) -> Optional[VarStatement]:
        var_token = self._token

        if not self._expect_peek(TokenType.IDENT):
            return None

        ident_stmt = Identifier(self._token, self._token.literal)

        if not self._expect_peek(TokenType.ASSIGN):
            return None

        # Loop until the end of the expression
        while self._token_is(TokenType.SEMICOLON):
            self._next_token()

        return VarStatement(token=var_token, name=ident_stmt)

    def _expect_peek(self, expect: TokenType) -> bool:
        if not self._peek_token_is(expect):
            error = ParsingError(
                f"Expected peek token to be {expect}, but peek was {self._peek_token.type}"
            )
            self.errors.append(error)
            return False

        self._next_token()
        return True

    def _token_is(self, other: TokenType):
        return self._token.type == other

    def _peek_token_is(self, other: TokenType):
        return self._peek_token.type == other

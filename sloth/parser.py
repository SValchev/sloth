from enum import IntEnum
from typing import Callable, Optional, Protocol
from .token import Token, TokenType
from .ast import (
    Expression,
    ExpressionStatement,
    Identifier,
    IntegerLiteral,
    PrefixExpression,
    Program,
    ReturnStatement,
    Statement,
    VarStatement,
)
from .lexer import Lexer


class ParsingError:
    def __init__(self, message: str) -> None:
        self.message = message


def parse_identifier(parser: "Parser") -> Identifier:
    return Identifier(parser._token, parser._token.literal)


def parse_integer(parser: "Parser") -> IntegerLiteral:
    value = parser._token.literal
    if not value.isnumeric():
        raise ValueError(f"Value expected to be integer but got {value}")

    return IntegerLiteral(parser._token, int(value))


def parse_prefix_expression(parser: "Parser") -> PrefixExpression:
    token = Token(literal=parser._token.literal, type=parser._token.type)

    parser._next_token()
    right_expression = parser._parse_expression(Precedence.PREFIX)

    return PrefixExpression(token, token.literal, right_expression)


class Precedence(IntEnum):
    LOWEST = 1
    PREFIX = 2

class ParseExpression(Protocol):
    def __call__(self, parser: "Parser") -> Expression: ...

class Parser:
    _PREFIX_REGISTRY: dict[TokenType, ParseExpression] = {
        TokenType.IDENT: parse_identifier,
        TokenType.INT: parse_integer,
        TokenType.BANG: parse_prefix_expression,
        TokenType.MINUS: parse_prefix_expression,
    }

    _INFIX_REGISTRY: dict[TokenType, Callable] = {}

    def __init__(self, lexer: Lexer) -> None:
        self.errors: list[ParsingError] = []
        self._lexer: Lexer = lexer

        self._token: Token = Token(TokenType.EOF, "")
        self._peek_token: Token = Token(TokenType.EOF, "")
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

    def _parse_statement(self) -> Statement | None:
        match self._token.type:
            case TokenType.VAR:
                return self._parse_var_stmt()
            case TokenType.RETURN:
                return self._parse_return_stmt()
        return self._parse_expression_stmt()

    def _next_token(self) -> Token:
        self._token = self._peek_token
        self._peek_token = self._lexer.next_token()
        return self._token

    def _parse_return_stmt(self) -> ReturnStatement:
        result = ReturnStatement(self._token)

        # Loop until the end of the expression
        while not self._token_is(TokenType.SEMICOLON):
            self._next_token()

        return result

    def _parse_expression(self, precedence: int) -> Expression | None:
        expression_token: Token = self._token

        prefix_parser: ParseExpression | None = self._PREFIX_REGISTRY.get(expression_token.type)

        if prefix_parser:
            return prefix_parser(self)

        infix_parser = self._INFIX_REGISTRY.get(expression_token.type)

        if infix_parser:
            return infix_parser(self)

        return None

    def _parse_expression_stmt(self) -> ExpressionStatement:
        expression: Optional[Expression] = self._parse_expression(Precedence.LOWEST)

        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()

        return ExpressionStatement(self._token, expression)

    def _parse_var_stmt(self) -> Optional[VarStatement]:
        var_token: Token = self._token
        if not self._expect_peek(TokenType.IDENT):
            return None
        ident_stmt = Identifier(self._token, self._token.literal)
        if not self._expect_peek(TokenType.ASSIGN):
            return None

        # Loop until the end of the expression
        while not self._token_is(TokenType.SEMICOLON):
            self._next_token()

        return VarStatement(token=var_token, name=ident_stmt)

    def _expect_peek(self, expect: TokenType) -> bool:
        if self._peek_token_is(expect):
            self._next_token()
            return True

        error = ParsingError(
            f"Expected peek token to be {expect}, but peek was {self._peek_token.type}"
        )
        self.errors.append(error)
        return False

    def _token_is(self, other: TokenType):
        return self._token.type == other

    def _peek_token_is(self, other: TokenType):
        return self._peek_token.type == other

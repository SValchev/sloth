from enum import IntEnum, auto
from typing import Optional, Protocol
from .token import Token, TokenType
from .ast import (
    Expression,
    ExpressionStatement,
    Identifier,
    InfixExpression,
    IntegerLiteral,
    PrefixExpression,
    Program,
    ReturnStatement,
    Statement,
    VarStatement,
    BooleanLiteral,
)
from .lexer import Lexer


class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


def parse_identifier(parser: "Parser") -> Identifier:
    return Identifier(parser._token, parser._token.literal)


def parse_integer(parser: "Parser") -> IntegerLiteral:
    value = parser._token.literal
    if not value.isnumeric():
        raise ValueError(f"Value expected to be integer but got {value}")

    return IntegerLiteral(parser._token, int(value))


def parse_boolean(parser: "Parser") -> BooleanLiteral:
    value = parser._token.literal
    if value not in (TokenType.FALSE, TokenType.TRUE):
        raise ValueError(f"Value expected to true or false but got {value}")

    value_return = value == TokenType.TRUE
    return BooleanLiteral(parser._token, value_return)


def parse_prefix_expression(parser: "Parser") -> PrefixExpression:
    token = Token.copy(parser._token)
    parser._next_token()
    right_expression = parser._parse_expression(Precedence.PREFIX)

    return PrefixExpression(token, token.literal, right_expression)


def parse_grouped_expression(parser: "Parser") -> Expression | None:
    parser._next_token()
    expression = parser._parse_expression(Precedence.LOWEST)

    if not parser._peek_token_is(TokenType.RPAREN):
        return

    parser._next_token()
    return expression


def parse_infix_expression(parser: "Parser", left: Expression) -> InfixExpression:
    token = Token.copy(parser._token)

    current_precedence: Precedence = parser._current_precedence()
    parser._next_token()
    right_expression: Expression | None = parser._parse_expression(current_precedence)

    return InfixExpression(token, token.literal, left, right_expression)


class Precedence(IntEnum):
    LOWEST = auto()
    EQUALS = auto()  # ==
    LESS_GREATER = auto()  # > or <
    SUM = auto()  # + or -
    PRODUCT = auto()  # / or *
    PREFIX = auto()  # -x or !x
    CALL = auto()  # my_function(call)


precedence_mapper = {
    TokenType.EQ: Precedence.EQUALS,
    TokenType.NOT_EQ: Precedence.EQUALS,
    TokenType.LT: Precedence.LESS_GREATER,
    TokenType.GT: Precedence.LESS_GREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,
    TokenType.SLASH: Precedence.PRODUCT,
    TokenType.ASTERISK: Precedence.PRODUCT,
}


class ParsePrefixExpression(Protocol):
    def __call__(self, parser: "Parser") -> Expression | None: ...


class ParseInfixExpression(Protocol):
    def __call__(self, parser: "Parser", left: Expression) -> Expression: ...


class Parser:
    _PREFIX_REGISTRY: dict[TokenType, ParsePrefixExpression] = {
        TokenType.IDENT: parse_identifier,
        TokenType.INT: parse_integer,
        TokenType.TRUE: parse_boolean,
        TokenType.FALSE: parse_boolean,
        TokenType.BANG: parse_prefix_expression,
        TokenType.MINUS: parse_prefix_expression,
        TokenType.LPAREN: parse_grouped_expression,
    }

    _INFIX_REGISTRY: dict[TokenType, ParseInfixExpression] = {
        TokenType.EQ: parse_infix_expression,
        TokenType.NOT_EQ: parse_infix_expression,
        TokenType.LT: parse_infix_expression,
        TokenType.GT: parse_infix_expression,
        TokenType.PLUS: parse_infix_expression,
        TokenType.MINUS: parse_infix_expression,
        TokenType.ASTERISK: parse_infix_expression,
        TokenType.SLASH: parse_infix_expression,
    }

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

    def _peek_precedence(self):
        return precedence_mapper.get(self._peek_token.type, Precedence.LOWEST)

    def _current_precedence(self):
        return precedence_mapper.get(self._token.type, Precedence.LOWEST)

    def _parse_expression(self, precedence: Precedence) -> Expression | None:
        expression_token: Token = self._token

        prefix_parser: ParsePrefixExpression | None = self._PREFIX_REGISTRY.get(
            expression_token.type
        )

        if not prefix_parser:
            self.errors.append(
                ParsingError(f"No prefix parser for {expression_token.type}")
            )
            return None

        left: Expression = prefix_parser(self)

        semicolon = TokenType.SEMICOLON
        while not self._token_is(semicolon) and precedence < self._peek_precedence():
            if self._peek_token.type not in self._INFIX_REGISTRY:
                return left

            infix: ParseInfixExpression = self._INFIX_REGISTRY[self._peek_token.type]

            self._next_token()
            left = infix(self, left)

        return left

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

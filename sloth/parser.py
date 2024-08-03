from enum import IntEnum, auto
from typing import Protocol
from .token import Token, TokenType
from .ast import (
    BlockStatement,
    CallExpression,
    Expression,
    ExpressionStatement,
    FunctionLiteral,
    Identifier,
    IfElseExpression,
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
        return None

    parser._next_token()
    return expression


def parse_infix_expression(parser: "Parser", left: Expression) -> InfixExpression:
    token = Token.copy(parser._token)

    current_precedence: Precedence = parser._current_precedence()
    parser._next_token()
    right_expression: Expression | None = parser._parse_expression(current_precedence)

    return InfixExpression(token, token.literal, left, right_expression)


def parse_block_statement(parser: "Parser") -> BlockStatement:
    token = parser._token.copy_self()
    stmts = []

    # The start of the body - {, skip it
    parser._assert_and_move(TokenType.LBRACE)

    while not parser._token_is(TokenType.RBRACE):
        if stmt := parser._parse_statement():
            stmts.append(stmt)
        parser._next_token()  # move to next stmt

    # current token is RBRACE, skip it - close the body
    parser._assert_and_move(TokenType.RBRACE)
    return BlockStatement(token, stmts)


def parse_if_else_statement(parser: "Parser") -> IfElseExpression | None:
    token = Token.copy(parser._token)

    if not parser._expect_peek(TokenType.LPAREN):
        return None

    condition = parser._parse_expression(Precedence.LOWEST)
    if not parser._expect_peek(TokenType.LBRACE):
        return None

    consequance: BlockStatement = parse_block_statement(parser)

    alternative = None
    if parser._token_is(TokenType.ELSE) and parser._expect_peek(TokenType.LBRACE):
        alternative = parse_block_statement(parser)

    return IfElseExpression(token, condition, consequance, alternative)


def parse_fn_arguments(parser: "Parser") -> list[Identifier]:
    parser._assert_and_move(TokenType.LPAREN)

    identifiers = []
    while not parser._token_is(TokenType.RPAREN):
        identifiers.append(parse_identifier(parser))
        parser._next_token()  # Skip current literal

        if parser._token_is(TokenType.COMMA):
            parser._next_token()  # Skip the comma

    parser._assert_and_move(TokenType.RPAREN)
    return identifiers


def parse_function_literal(parser: "Parser") -> FunctionLiteral | None:
    token = Token.copy(parser._token)
    if not parser._expect_peek(TokenType.LPAREN):
        return None

    arguments = parse_fn_arguments(parser)

    if not parser._token_is(TokenType.LBRACE):
        return None

    body: BlockStatement = parse_block_statement(parser)

    return FunctionLiteral(token, arguments, body)


def parse_call_arguments(parser: "Parser") -> list[Expression]:
    parser._assert_and_move(TokenType.LPAREN)
    if parser._token_is(TokenType.RPAREN):
        return []

    exp = parser._parse_expression(Precedence.LOWEST)
    if exp is None:
        raise ValueError()

    args = [exp]

    while parser._peek_token_is(TokenType.COMMA):
        parser._next_token()
        parser._next_token()

        exp = parser._parse_expression(Precedence.LOWEST)
        if exp is None:
            raise ValueError()
        args.append(exp)

    if not parser._expect_peek(TokenType.RPAREN):
        return []

    return args


def parse_call_expression(parser: "Parser", left: Expression) -> CallExpression:
    token = Token.copy(parser._token)
    args = parse_call_arguments(parser)
    return CallExpression(token, left, args)


def parse_var_statement(parser: "Parser") -> VarStatement | None:
    var_token: Token = parser._token
    if not parser._expect_peek(TokenType.IDENT):
        return None

    ident_stmt = Identifier(parser._token, parser._token.literal)
    if not parser._expect_peek(TokenType.ASSIGN):
        return None

    parser._next_token()  # Move assign

    exp = parser._parse_expression(Precedence.LOWEST)

    if parser._peek_token_is(TokenType.SEMICOLON):
        parser._next_token()

    return VarStatement(var_token, ident_stmt, exp)


def parse_return_statement(parser: "Parser") -> ReturnStatement:
    token = parser._token.copy_self()

    parser._next_token()
    exp = parser._parse_expression(Precedence.LOWEST)

    if parser._peek_token_is(TokenType.SEMICOLON):
        parser._next_token()

    return ReturnStatement(token, exp)


def parse_expression_statement(parser: "Parser") -> ExpressionStatement:
    expression: Expression | None = parser._parse_expression(Precedence.LOWEST)

    if parser._peek_token_is(TokenType.SEMICOLON):
        parser._next_token()

    return ExpressionStatement(parser._token, expression)


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
    TokenType.LPAREN: Precedence.CALL,
}


class ParsePrefixExpression(Protocol):
    def __call__(self, parser: "Parser") -> Expression | None: ...


class ParseInfixExpression(Protocol):
    def __call__(self, parser: "Parser", left: Expression) -> Expression: ...


class Parser:
    _PREFIX_REGISTRY: dict[TokenType, ParsePrefixExpression] = {
        TokenType.FUNC: parse_function_literal,
        TokenType.IF: parse_if_else_statement,
        TokenType.IDENT: parse_identifier,
        TokenType.INT: parse_integer,
        TokenType.TRUE: parse_boolean,
        TokenType.FALSE: parse_boolean,
        TokenType.BANG: parse_prefix_expression,
        TokenType.MINUS: parse_prefix_expression,
        TokenType.LPAREN: parse_grouped_expression,
    }

    _INFIX_REGISTRY: dict[TokenType, ParseInfixExpression] = {
        TokenType.LPAREN: parse_call_expression,
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
                return parse_var_statement(self)
            case TokenType.RETURN:
                return parse_return_statement(self)
        return parse_expression_statement(self)

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

    def _next_token(self) -> Token:
        self._token = self._peek_token
        self._peek_token = self._lexer.next_token()
        return self._token

    def _peek_precedence(self):
        return precedence_mapper.get(self._peek_token.type, Precedence.LOWEST)

    def _current_precedence(self):
        return precedence_mapper.get(self._token.type, Precedence.LOWEST)

    def _assert_and_move(self, current_type: TokenType):
        assert self._token_is(
            current_type
        ), f"Token {self._token} is but expected {current_type}"

        self._next_token()

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

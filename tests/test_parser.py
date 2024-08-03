from dataclasses import dataclass
import builtins
from math import exp

from sloth.ast import (
    BlockStatement,
    BooleanLiteral,
    Expression,
    ExpressionStatement,
    FunctionLiteral,
    Identifier,
    InfixExpression,
    IntegerLiteral,
    PrefixExpression,
    ReturnStatement,
    VarStatement,
    IfElseExpression,
)
from sloth.parser import Parser
from sloth.token import TokenType


def test_var_parser():
    input_ = """var five = 5;
    var ten = 10;
    var one_hundred = 100;
    """

    parser = Parser.from_input(input_)

    program = parser.parse_program()

    expected_identifiers = ["five", "ten", "one_hundred"]

    assert len(program.statements) == len(expected_identifiers)
    assert not parser.errors

    for stmt, expected_ident in zip(program.statements, expected_identifiers):
        assert isinstance(stmt, VarStatement)
        assert stmt.token.type == TokenType.VAR
        assert stmt.token.literal == "var"

        ident = stmt.name
        assert isinstance(ident, Identifier)
        assert ident.token.type == TokenType.IDENT
        assert ident.value == expected_ident


def test_parser_generate_errors_with_var_statement():
    input_ = """var five 5;
    var = 10;
    var 100;
    """

    parser = Parser.from_input(input_)
    parser.parse_program()

    assert len(parser.errors) == 4


def test_return_parser():
    input_ = """return 5;
    return 10;
    return add(x, y);
    """

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 3
    assert not parser.errors

    for stmt in program.statements:
        assert isinstance(stmt, ReturnStatement)
        assert stmt.token.type == TokenType.RETURN
        assert stmt.token.literal == "return"

        assert not stmt.expression


def test_identifier_expression_parser():
    input_ = """foo;
    bar
    """

    expected_idents = ["foo", "bar"]

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 2
    assert not parser.errors

    for ei, stmt in zip(expected_idents, program.statements):
        assert isinstance(stmt, ExpressionStatement)

        assert isinstance(stmt.expression, Identifier)
        assert stmt.expression.token.type == TokenType.IDENT
        assert stmt.expression.value == ei
        assert stmt.expression.token.literal == ei


def test_boolean_expression_parser():
    input_ = """true;
    false 
    """

    expected_idents = [True, False]

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 2
    assert not parser.errors

    for ei, stmt in zip(expected_idents, program.statements):
        assert isinstance(stmt, ExpressionStatement)

        assert isinstance(stmt.expression, BooleanLiteral)
        assert stmt.expression.value == ei
        assert stmt.expression.token.literal == str(ei).lower()


def test_integer_expression_parser():
    input_ = """5
    10;
    100 
    """

    expected = [5, 10, 100]

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 3
    assert not parser.errors

    for e, stmt in zip(expected, program.statements):
        assert isinstance(stmt, ExpressionStatement)
        _check_expression_stmt_integer(stmt.expression, e)


def test_prefix_expression_parser():
    input_ = """!10;
    -5;
    !true;
    !false;
    """

    expected = [
        ("!10", "!", 10),
        ("-5", "-", 5),
        ("!true", "!", True),
        ("!false", "!", False),
    ]

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 4
    assert not parser.errors

    for e, stmt in zip(expected, program.statements):
        literal, prefix, as_value = e
        assert isinstance(stmt, ExpressionStatement)
        assert isinstance(stmt.expression, PrefixExpression)
        prefix_stmt = stmt.expression
        assert prefix_stmt.token.type == prefix
        assert prefix_stmt.operator == prefix
        _check_expression_stmt_by_type(prefix_stmt.right, as_value)


def test_function_literal_parser():
    input_ = """func(x, y) { 
        x + y
    }
    """
    expected = "func(x, y) { (x + y) }"

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 1
    assert isinstance(program.statements[0], ExpressionStatement)
    assert isinstance(program.statements[0].expression, FunctionLiteral)

    fn = program.statements[0].expression

    assert len(fn.arguments) == 2
    for ident, name in zip(fn.arguments, ["x", "y"]):
        assert isinstance(ident, Identifier)
        assert ident.value == name

    assert isinstance(fn.body, BlockStatement)

    assert str(fn) == expected


def test_function_argument_parser():
    input_ = [
        "func(x, y) {}",
        "func() {}",
    ]  # "func(1 + 2, 3 + 4) {}"]
    expected = [
        ("x", "y"),
        [],
    ]  # ["(1 + 2)", "(3 + 4)"]]

    for i, e in zip(input_, expected):
        _test_argument_parser(i, e)


def _test_argument_parser(input_, arguments: list):
    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 1
    assert isinstance(program.statements[0], ExpressionStatement)
    assert isinstance(program.statements[0].expression, FunctionLiteral)

    fn = program.statements[0].expression

    assert len(fn.arguments) == len(arguments)
    for ident, arg in zip(fn.arguments, arguments):
        assert ident.value == arg


def test_if_else_expression_parser():
    """if (<condition>) { consequence } else { <alternative> }"""
    input_ = """if (1 == 5) {
        x
    } else {
        y
    }
    """

    expected = "if (1 == 5) { x } else { y }"

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 1
    assert not parser.errors

    assert isinstance(program.statements[0], ExpressionStatement)
    assert isinstance(program.statements[0].expression, IfElseExpression)
    if_else_stmt = program.statements[0].expression

    assert if_else_stmt.condition
    assert isinstance(if_else_stmt.condition, Expression)

    assert len(if_else_stmt.consequence.body) == 1
    assert isinstance(if_else_stmt.consequence, BlockStatement)

    assert if_else_stmt.alternative
    assert len(if_else_stmt.alternative.body) == 1

    assert if_else_stmt.token.type == TokenType.IF

    assert str(if_else_stmt) == expected


def test_infix_expression_parser():
    input_ = """
    5 + 5;
    5 - 5;
    5 > 5;
    5 < 5;
    5 == 5;
    5 != 5;
    5 * 5;
    5 / 5;
    true == true
    true != true
    false == true
    """

    @dataclass(frozen=True)
    class Expected:
        value: str
        left: int
        operand: str
        right: int

    expected = [
        Expected(*x)
        for x in [
            ("5 + 5", 5, "+", 5),
            ("5 - 5", 5, "-", 5),
            ("5 > 5", 5, ">", 5),
            ("5 < 5", 5, "<", 5),
            ("5 == 5", 5, "==", 5),
            ("5 != 5", 5, "!=", 5),
            ("5 * 5", 5, "*", 5),
            ("5 / 5", 5, "/", 5),
            ("true == true", True, "==", True),
            ("true != true", True, "!=", True),
            ("false == true", False, "==", True),
        ]
    ]

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == len(expected)
    assert not parser.errors

    for e, stmt in zip(expected, program.statements):
        assert isinstance(stmt, ExpressionStatement)
        assert isinstance(stmt.expression, InfixExpression)

        stmt = stmt.expression
        assert stmt.token.type == e.operand
        assert stmt.operator == e.operand

        _check_expression_stmt_by_type(stmt.right, e.right)
        _check_expression_stmt_by_type(stmt.left, e.left)


def _check_expression_stmt_by_type(expression, value):
    match type(value):
        case builtins.int:
            _check_expression_stmt_integer(expression, value)
        case builtins.bool:
            _check_expression_stmt_boolean(expression, value)
        case _:
            raise ValueError("This should never happen")


def _check_expression_stmt_integer(expression, expected: int):
    assert isinstance(expression, IntegerLiteral)
    assert expression.token.type == TokenType.INT
    assert expression.value == expected
    assert expression.token.literal == str(expected)


def _check_expression_stmt_boolean(expression, expected: bool):
    assert isinstance(expression, BooleanLiteral)
    assert expression.token.type in (TokenType.FALSE, TokenType.TRUE)
    assert expression.value == expected
    assert expression.token.literal == str(expected).lower()


def test_operator_precedence():
    tests = [
        ("-a * b", "((-a) * b)"),
        ("!-a", "(!(-a))"),
        ("a + b + c", "((a + b) + c)"),
        ("a + b - c", "((a + b) - c)"),
        ("a * b * c", "((a * b) * c)"),
        ("a * b / c", "((a * b) / c)"),
        ("a + b / c", "(a + (b / c))"),
        ("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"),
        ("3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"),
        ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),
        ("5 > 4 != 3 < 4", "((5 > 4) != (3 < 4))"),
        ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
        ("5 > 3 == true", "((5 > 3) == true)"),
        ("5 > 3 == false", "((5 > 3) == false)"),
        ("a + (b + c)", "(a + (b + c))"),
        ("a * (b / c)", "(a * (b / c))"),
        ("a * (b + c)", "(a * (b + c))"),
        ("a * (b + c) / d", "((a * (b + c)) / d)"),
    ]

    for input_, expected in tests:
        parser = Parser.from_input(input_)
        program = parser.parse_program()
        assert str(program) == expected

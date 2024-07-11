from dataclasses import dataclass

from sloth.ast import (
    ExpressionStatement,
    Identifier,
    InfixExpression,
    IntegerLiteral,
    PrefixExpression,
    ReturnStatement,
    VarStatement,
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
    """

    expected = [
        ("!10", "!", 10),
        ("-5", "-", 5),
    ]

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    assert len(program.statements) == 2
    assert not parser.errors

    for e, stmt in zip(expected, program.statements):
        literal, prefix, as_int = e
        assert isinstance(stmt, ExpressionStatement)
        assert isinstance(stmt.expression, PrefixExpression)
        prefix_stmt = stmt.expression
        assert prefix_stmt.token.type == prefix
        assert prefix_stmt.operator == prefix

        _check_expression_stmt_integer(prefix_stmt.right, as_int)


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

        _check_expression_stmt_integer(stmt.right, e.right)
        _check_expression_stmt_integer(stmt.left, e.left)


def _check_expression_stmt_integer(expression, expected: int):
    assert isinstance(expression, IntegerLiteral)
    assert expression.token.type == TokenType.INT
    assert expression.value == expected
    assert expression.token.literal == str(expected)


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
    ]

    for input_, expected in tests:
        parser = Parser.from_input(input_)
        program = parser.parse_program()
        print(parser.errors)
        print(program)
        print("-" * 100)
        print("\n" * 3)
        assert str(program) == expected

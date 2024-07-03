from sloth.ast import ReturnStatement, VarStatement
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

        assert stmt.name.token.type == TokenType.IDENT
        assert stmt.name.value == expected_ident


def test_parser_generate_errors_with_var_statement():
    input_ = """var five 5;
    var = 10;
    var 100;
    """

    parser = Parser.from_input(input_)
    parser.parse_program()

    assert len(parser.errors) == 3


def test_return_parser():
    input_ = """ return 5;
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
    input_ = """ var a = 5;
    var b = 10;
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

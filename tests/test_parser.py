from sloth.ast import Statement, VarStatement
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

    for stmt, expected_ident in zip(program.statements, expected_identifiers):
        _test_var_stmt(stmt, expected_ident)

    pass


def _test_var_stmt(stmt: Statement, expected_identifier: str):
    assert isinstance(stmt, VarStatement)
    assert stmt.token.type == TokenType.VAR
    assert stmt.token.literal == "var"

    assert stmt.name.token.type == TokenType.IDENT
    assert stmt.name.value == expected_identifier

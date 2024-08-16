from sloth.token import TokenType
from tests.helpers import validate_input


def test_next_token_input1():
    input_ = """var  forty = 40;
    var two = 2;
    
    var add = func(x, y) {
        x + y
    };

    var name = "Stan"
    
    var result = func(forty, two);
    """

    expected = [
        # Row one
        (TokenType.VAR, "var"),
        (TokenType.IDENT, "forty"),
        (TokenType.ASSIGN, "="),
        (TokenType.INT, "40"),
        (TokenType.SEMICOLON, ";"),
        # Rwo two
        (TokenType.VAR, "var"),
        (TokenType.IDENT, "two"),
        (TokenType.ASSIGN, "="),
        (TokenType.INT, "2"),
        (TokenType.SEMICOLON, ";"),
        # Function
        (TokenType.VAR, "var"),
        (TokenType.IDENT, "add"),
        (TokenType.ASSIGN, "="),
        (TokenType.FUNC, "func"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENT, "x"),
        (TokenType.COMMA, ","),
        (TokenType.IDENT, "y"),
        (TokenType.RPAREN, ")"),
        (TokenType.LBRACE, "{"),
        (TokenType.IDENT, "x"),
        (TokenType.PLUS, "+"),
        (TokenType.IDENT, "y"),
        (TokenType.RBRACE, "}"),
        (TokenType.SEMICOLON, ";"),
        # name = Stan
        (TokenType.VAR, "var"),
        (TokenType.IDENT, "name"),
        (TokenType.ASSIGN, "="),
        (TokenType.STRING, "Stan"),
        # result
        (TokenType.VAR, "var"),
        (TokenType.IDENT, "result"),
        (TokenType.ASSIGN, "="),
        (TokenType.FUNC, "func"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENT, "forty"),
        (TokenType.COMMA, ","),
        (TokenType.IDENT, "two"),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
    ]

    validate_input(input_, expected)


def test_next_token_input2():
    input_ = """if(5 > 10){
        return true
    } else {
        return false
    }
    """

    expected = [
        # Row one
        (TokenType.IF, "if"),
        (TokenType.LPAREN, "("),
        (TokenType.INT, "5"),
        (TokenType.GT, ">"),
        (TokenType.INT, "10"),
        (TokenType.RPAREN, ")"),
        # Rwo two
        (TokenType.LBRACE, "{"),
        (TokenType.RETURN, "return"),
        (TokenType.TRUE, "true"),
        (TokenType.RBRACE, "}"),
        (TokenType.ELSE, "else"),
        # Function
        (TokenType.LBRACE, "{"),
        (TokenType.RETURN, "return"),
        (TokenType.FALSE, "false"),
        (TokenType.RBRACE, "}"),
    ]

    validate_input(input_, expected)


def test_next_token_equal():
    input_ = """1 == 42
    1 != 42
    """

    expected = [
        # Row one
        (TokenType.INT, "1"),
        (TokenType.EQ, "=="),
        (TokenType.INT, "42"),
        # Rwo two
        (TokenType.INT, "1"),
        (TokenType.NOT_EQ, "!="),
        (TokenType.INT, "42"),
    ]

    validate_input(input_, expected)


def test_string():
    input = '"Hello World"'
    expected = [
        (TokenType.STRING, "Hello World"),
    ]

    validate_input(input, expected)


def test_bool():
    input_ = """true == false
    false != true
    """

    expected = [
        # Row one
        (TokenType.TRUE, "true"),
        (TokenType.EQ, "=="),
        (TokenType.FALSE, "false"),
        # Rwo two
        (TokenType.FALSE, "false"),
        (TokenType.NOT_EQ, "!="),
        (TokenType.TRUE, "true"),
    ]

    validate_input(input_, expected)

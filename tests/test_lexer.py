from sloth.lexer import Lexer
from sloth.token import TokenType


def test_next_token():
    input_ = """var forty = 40;
    var two = 2;
    
    var add = func(x, y) {
        x + y
    };
    
    var result = func(forty, two);
    """

    expected = [
        (TokenType.VAR, "var"),
        (TokenType.IDENT, "forty"),
        (TokenType.ASSIGN, "="),
        (TokenType.INT, "40"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.VAR, "var"),
        (TokenType.IDENT, "two"),
        (TokenType.ASSIGN, "="),
        (TokenType.INT, "2"),
        (TokenType.SEMICOLON, ";"),
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

    lexer = Lexer(input_)

    for token_type, literal in expected:
        token = lexer.next_token()

        assert token.literal == literal
        assert token.type == token_type

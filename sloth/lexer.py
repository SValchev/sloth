from .token import Token, TokenType


class Lexer:
    def __init__(self, input_: str) -> None:
        self._input: str = input_
        self._position: int = 0
        self._read_position: int = 0
        self._char: str

        self._read_char()

    def _read_char(self) -> None:
        if self._read_position >= len(self._input):
            self._char = "\00"
        else:
            self._char = self._input[self._read_position]

        self._position = self._read_position
        self._read_position += 1

    def next_token(self) -> Token:

        token = None
        match self._char:
            case TokenType.ASSIGN:
                token = Token(TokenType.ASSIGN, self._char)
            case TokenType.PLUS:
                token = Token(TokenType.PLUS, self._char)
            case TokenType.LPAREN:
                token = Token(TokenType.LPAREN, self._char)
            case TokenType.RPAREN:
                token = Token(TokenType.RPAREN, self._char)
            case TokenType.LBRACE:
                token = Token(TokenType.LBRACE, self._char)
            case TokenType.RBRACE:
                token = Token(TokenType.RBRACE, self._char)
            case TokenType.SEMICOLON:
                token = Token(TokenType.SEMICOLON, self._char)
            case TokenType.COMMA:
                token = Token(TokenType.COMMA, self._char)
            case "\00":
                token = Token(TokenType.EOF, "")
            case _:
                raise NotImplementedError()

        self._read_char()
        return token

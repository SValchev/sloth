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

    def _char_is_letter(self) -> bool:
        return self._char.isalpha() or self._char == "_"

    def _read_word(self) -> str:
        position = self._position
        while self._char_is_letter():
            self._read_char()

        return self._input[position : self._position]

    def _char_is_digit(self) -> bool:
        return self._char.isnumeric()

    def _read_digit(self) -> str:
        position = self._position
        while self._char_is_digit():
            self._read_char()

        return self._input[position : self._position]

    def _consume_spaces(self) -> None:
        while self._char.isspace():
            self._read_char()

    def _peek_char(self) -> str:
        if self._read_position >= len(self._input):
            return "\00"
        return self._input[self._read_position]

    def next_token(self) -> Token:
        self._consume_spaces()
        token = None
        match self._char:
            case TokenType.ASSIGN:
                if self._peek_char() == '=':
                    self._read_char()
                    token = Token(TokenType.EQ, TokenType.EQ)
                else:
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
            case TokenType.GT:
                token = Token(TokenType.GT, self._char)
            case TokenType.LT:
                token = Token(TokenType.LT, self._char)
            case TokenType.BANG:
                if self._peek_char() == '=':
                    self._read_char()
                    token = Token(TokenType.NOT_EQ, TokenType.NOT_EQ)
                else:
                    token = Token(TokenType.BANG, self._char)
            case TokenType.ASTERISK:
                token = Token(TokenType.ASTERISK, self._char)
            case TokenType.SLASH:
                token = Token(TokenType.SLASH, self._char)
            case "\00":
                token = Token(TokenType.EOF, "")
            case _:
                if self._char_is_letter():
                    # Can return keyword or identifier
                    return Token.from_word(self._read_word())
                elif self._char_is_digit():
                    return Token(TokenType.INT, self._read_digit())
                else:
                    token = Token(TokenType.ILLEGAL, "")
        
        self._read_char()
        return token
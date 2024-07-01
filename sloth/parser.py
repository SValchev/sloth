from .token import Token, TokenType
from sloth.ast import Identifier, Program, VarStatement
from .lexer import Lexer


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer: Lexer = lexer

        self._token: Token = None
        self._peek_token: Token = None

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

    def _parse_statement(self):
        match self._token.type:
            case TokenType.VAR:
                return self._parse_var_stmt()
        return None

    def _next_token(self) -> Token:
        self._token = self._peek_token
        self._peek_token = self._lexer.next_token()
        return self._token

    def _parse_var_stmt(self) -> VarStatement:
        var_token = self._token

        if not self._peek_token_is(TokenType.IDENT):
            raise ValueError()

        ident = self._next_token()

        if not self._peek_token_is(TokenType.ASSIGN):
            raise ValueError()

        # Loop until the end of the expression
        while self._token_is(TokenType.SEMICOLON):
            self._next_token()

        ident_stmt = Identifier(ident, ident.literal)
        return VarStatement(token=var_token, name=ident_stmt)

    def _token_is(self, other: TokenType):
        return self._token.type == other

    def _peek_token_is(self, other: TokenType):
        return self._peek_token.type == other

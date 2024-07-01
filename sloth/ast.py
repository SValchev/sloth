from typing import Optional, Protocol
from .token import Token


class Node(Protocol):
    def token_literal(self) -> str: ...


class Statement(Node, Protocol):
    def statement_node(self): ...


class Expression(Node, Protocol):
    def expression_node(self): ...


class Program(Node):
    def __init__(self) -> None:
        self.statements: list[Statement] = []

    def token_literal(self) -> str:
        if not self.statements:
            return ""
        return self.statements[0].token_literal()

    def add_statement(self, statement: Statement):
        self.statements.append(statement)


class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value

    def expression_node(self):
        raise NotImplementedError()

    def token_literal(self) -> str:
        return self.token.literal


class VarStatement(Statement):
    def __init__(
        self, token: Token, name: Identifier, value: Optional[Expression] = None
    ) -> None:
        self.token: Token = token
        self.name: Identifier = name
        self.value: Optional[Expression] = value

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self):
        raise NotImplementedError()


class ReturnStatement(Statement):
    def __init__(self, token, expression: Optional[Expression] = None) -> None:
        self.token: Token = token
        self.expression: Optional[Expression] = expression

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self):
        raise NotImplementedError()

from abc import ABC, abstractmethod
from typing import Optional
from .token import Token


class Node(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass


class Statement(Node):
    @abstractmethod
    def _statement_node(self):
        pass


class Expression(Node):
    @abstractmethod
    def _expression_node(self):
        pass


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

    def _expression_node(self):
        return super()._expression_node()

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

    def _statement_node(self):
        return super()._statement_node()

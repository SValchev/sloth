from abc import ABC, abstractmethod
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


class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self._token = token
        self._value = value

    def _expression_node(self):
        return super()._expression_node()


class VarStatement(Statement):
    def __init__(self, token: Token, name: Identifier, value: Expression) -> None:
        self._token: Token = token
        self._name: Identifier = name
        self._value: Expression = value

    def token_literal(self) -> str:
        return self._token.literal

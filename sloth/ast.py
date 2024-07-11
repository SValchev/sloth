from dataclasses import dataclass
from typing import Optional, Protocol
from .token import Token


class Node(Protocol):
    def token_literal(self) -> str: ...

    def __str__(self) -> str: ...


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

    def __str__(self) -> str:
        return "".join(map(str, self.statements))


@dataclass(frozen=True)
class IntegerLiteral(Expression):
    token: Token
    value: int

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Identifier(Expression):
    """
    var x = 5;
    Where the :value: is the name of the identifier
    """

    token: Token
    value: str

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class VarStatement(Statement):
    token: Token
    name: Identifier
    value: Optional[Expression] = None

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"{self.token.literal} {self.name} = {self.value};"


@dataclass(frozen=True)
class ReturnStatement(Statement):
    token: Token
    expression: Optional[Expression] = None

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"return {self.expression};"


@dataclass(frozen=True)
class ExpressionStatement(Statement):
    """Used for one line expressions to be wrapped as statement, so they can me added to the Program/root
    example:
        x + 10
        5 + 5
    """

    token: Token
    expression: Optional[Expression]

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        if not self.expression:
            return ""
        return str(self.expression)


@dataclass(frozen=True)
class PrefixExpression(Expression):
    token: Token
    operator: str
    right: Optional[Expression]

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"({self.token.literal}{self.right})"


@dataclass(frozen=True)
class InfixExpression(Expression):
    token: Token
    operator: str
    left: Expression | None
    right: Expression | None

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"

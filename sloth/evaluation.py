from typing import Any
from .ast import (
    BlockStatement,
    BooleanLiteral,
    Expression,
    ExpressionStatement,
    IfElseExpression,
    InfixExpression,
    IntegerLiteral,
    Node,
    PrefixExpression,
    Program,
    ReturnStatement,
    Statement,
)

from .objects import Boolean, Fault, Integer, Null


# Native constants
TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()
ZERO = Integer(0)


class ReturnStopExcexution(Exception):
    def __init__(self, expression: Expression, *args) -> None:
        self.expression = expression
        super().__init__(*args)


class FaultStopExcexution(Exception):
    def __init__(self, msg: str, *args) -> None:
        self.fault = Fault(msg)
        super().__init__(*args)


def _native_to_boolean(native: bool) -> Boolean:
    assert isinstance(native, bool)

    return TRUE if native else FALSE


def evaluate_statements(statements: list[Statement]) -> Any:
    result = None
    for stmt in statements:
        try:
            result = evaluate(stmt)
        except ReturnStopExcexution as e:
            # No need to continue the body of the execution
            return evaluate(e.expression)
        except FaultStopExcexution as e:
            return e.fault  # No need to continue the body of the execution

    return result


def evaluate_prefix_boolean(boolean: BooleanLiteral):
    return FALSE if boolean.value else TRUE


def evaluate_prefix_bang(expression: PrefixExpression) -> Boolean | Null:
    evaluated = evaluate(expression.right)

    if evaluated == TRUE:
        return FALSE
    elif evaluated == FALSE:
        return TRUE
    elif isinstance(evaluated, Integer):
        return FALSE

    return NULL


def evaluate_prefix_minus(expression: PrefixExpression) -> Integer | Null:
    evaluated = evaluate(expression.right)

    if not isinstance(evaluated, Integer):
        return NULL

    return Integer(value=-evaluated.value)


def evaluate_prefix_expression(node: PrefixExpression) -> Integer | Boolean | Null:
    match node:
        case PrefixExpression(operator="!"):
            return evaluate_prefix_bang(node)
        case PrefixExpression(operator="-"):
            return evaluate_prefix_minus(node)
        case _:
            raise FaultStopExcexution.from_str("")


def evaluate_integer_infix_expression(
    left: Integer, right: Integer, operator: str
) -> Integer | Boolean | Null:
    match operator:
        case "+":
            return Integer(left.value + right.value)
        case "-":
            return Integer(left.value - right.value)
        case "*":
            return Integer(left.value * right.value)
        case "/":
            if right.value == 0:
                raise FaultStopExcexution.from_str("can not divide by zero")
            return Integer(left.value // right.value)
        case "==":
            return _native_to_boolean(left.value == right.value)
        case "!=":
            return _native_to_boolean(left.value != right.value)
        case ">":
            return _native_to_boolean(left.value > right.value)
        case "<":
            return _native_to_boolean(left.value < right.value)
        case _:
            return NULL


def evaluate_boolean_infix_expression(left: Boolean, right: Boolean, operator: str):
    match operator:
        case "==":
            return _native_to_boolean(left.value == right.value)
        case "!=":
            return _native_to_boolean(left.value != right.value)
        case _:
            return NULL


def evaluate_infix_expression(infix: InfixExpression):
    left = evaluate(infix.left)
    right = evaluate(infix.right)

    match left, right:
        case Integer(), Integer():
            return evaluate_integer_infix_expression(left, right, infix.operator)
        case Boolean(), Boolean():
            return evaluate_boolean_infix_expression(left, right, infix.operator)
        case _:
            raise NotImplementedError(f"{left} and {right} combination not implemented")


def evaluate_if_else_expression(if_else: IfElseExpression):
    eval_condition = evaluate(if_else.condition)

    if eval_condition in (FALSE, NULL, ZERO):
        return evaluate(if_else.alternative) if if_else.alternative else NULL
    return evaluate(if_else.consequence)


def evaluate_return_statement(return_stmt: ReturnStatement):
    raise ReturnStopExcexution(return_stmt.expression)


def evaluate(node: Node):
    match node:
        case Program():
            return evaluate_statements(node.statements)
        case BlockStatement():
            return evaluate_statements(node.body)
        case ExpressionStatement():
            return evaluate(node.expression)
        case IntegerLiteral():
            return Integer(node.value)
        case BooleanLiteral():
            return _native_to_boolean(node.value)
        case PrefixExpression():
            return evaluate_prefix_expression(node)
        case InfixExpression():
            return evaluate_infix_expression(node)
        case IfElseExpression():
            return evaluate_if_else_expression(node)
        case ReturnStatement():
            return evaluate_return_statement(node)
        case _:
            raise NotImplementedError(f"{type(node)} is still not implemented")

from typing import Any
from .ast import (
    BlockStatement,
    BooleanLiteral,
    Expression,
    ExpressionStatement,
    Identifier,
    IfElseExpression,
    InfixExpression,
    IntegerLiteral,
    Node,
    PrefixExpression,
    Program,
    ReturnStatement,
    Statement,
    VarStatement,
)

from .objects import Boolean, Fault, Integer, Null


# Native constants
TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()
ZERO = Integer(0)


class Environment(dict):
    pass


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


def evaluate_statements(statements: list[Statement], env: Environment) -> Any:
    result = None
    for stmt in statements:
        try:
            result = evaluate(stmt, env)
        except ReturnStopExcexution as e:
            # No need to continue the body of the execution
            return evaluate(e.expression, env)
        except FaultStopExcexution as e:
            return e.fault  # No need to continue the body of the execution

    return result


def evaluate_prefix_boolean(boolean: BooleanLiteral):
    return FALSE if boolean.value else TRUE


def evaluate_prefix_bang(
    expression: PrefixExpression, env: Environment
) -> Boolean | Null:
    evaluated = evaluate(expression.right, env)

    if evaluated == TRUE:
        return FALSE
    elif evaluated == FALSE:
        return TRUE
    elif isinstance(evaluated, Integer):
        return FALSE

    return NULL


def evaluate_prefix_minus(
    expression: PrefixExpression, env: Environment
) -> Integer | Null:
    evaluated = evaluate(expression.right, env)

    if not isinstance(evaluated, Integer):
        return NULL

    return Integer(value=-evaluated.value)


def evaluate_prefix_expression(
    node: PrefixExpression, env: Environment
) -> Integer | Boolean | Null:
    match node:
        case PrefixExpression(operator="!"):
            return evaluate_prefix_bang(node, env)
        case PrefixExpression(operator="-"):
            return evaluate_prefix_minus(node, env)
        case _:
            raise FaultStopExcexution("")


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
                raise FaultStopExcexution("can not divide by zero")
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


def evaluate_infix_expression(infix: InfixExpression, env):
    left = evaluate(infix.left, env)
    right = evaluate(infix.right, env)

    match left, right:
        case Integer(), Integer():
            return evaluate_integer_infix_expression(left, right, infix.operator)
        case Boolean(), Boolean():
            return evaluate_boolean_infix_expression(left, right, infix.operator)
        case _:
            raise NotImplementedError(f"{left} and {right} combination not implemented")


def evaluate_if_else_expression(if_else: IfElseExpression, env: Environment):
    eval_condition = evaluate(if_else.condition, env)

    if eval_condition in (FALSE, NULL, ZERO):
        return evaluate(if_else.alternative, env) if if_else.alternative else NULL
    return evaluate(if_else.consequence, env)


def evaluate_return_statement(return_stmt: ReturnStatement):
    raise ReturnStopExcexution(return_stmt.expression)


def evaluate_var_statement(var_stmt: VarStatement, env: Environment):
    name = var_stmt.name_value()
    env[name] = evaluate(var_stmt.value, env)


def evaluate_identifier(ident: Identifier, env: Environment):
    name = ident.value

    if name not in env:
        raise FaultStopExcexution(f"name {name} is not defined")
    return env[name]


def evaluate(node: Node, env: Environment):
    match node:
        case Program():
            return evaluate_statements(node.statements, env)
        case BlockStatement():
            return evaluate_statements(node.body, env)
        case ExpressionStatement():
            return evaluate(node.expression, env)
        case IntegerLiteral():
            return Integer(node.value)
        case BooleanLiteral():
            return _native_to_boolean(node.value)
        case PrefixExpression():
            return evaluate_prefix_expression(node, env)
        case InfixExpression():
            return evaluate_infix_expression(node, env)
        case IfElseExpression():
            return evaluate_if_else_expression(node, env)
        case ReturnStatement():
            return evaluate_return_statement(node)
        case VarStatement():
            return evaluate_var_statement(node, env)
        case Identifier():
            return evaluate_identifier(node, env)
        case _:
            raise NotImplementedError(f"{type(node)} is still not implemented")

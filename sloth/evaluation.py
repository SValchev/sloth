from .ast import (
    BooleanLiteral,
    Expression,
    ExpressionStatement,
    InfixExpression,
    IntegerLiteral,
    Node,
    PrefixExpression,
    Program,
)

from .objects import Boolean, Integer, Null


# Native constants
TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def _native_to_boolean(native: bool) -> Boolean:
    assert isinstance(native, bool)

    return TRUE if native else FALSE


def evaluate_program(program: Program):
    result = None
    for stmt in program.statements:
        result = evaluate(stmt)

    return result


def evaluate_prefix_boolean(boolean: BooleanLiteral):
    return FALSE if boolean.value else TRUE


def evaluate_prefix_bang(expression: PrefixExpression):
    evaluated = evaluate(expression.right)

    if evaluated == TRUE:
        return FALSE
    elif evaluated == FALSE:
        return TRUE
    elif isinstance(evaluated, Integer):
        return FALSE

    return NULL


def evaluate_prefix_minus(expression: PrefixExpression):
    evaluated = evaluate(expression.right)

    if not isinstance(evaluated, Integer):
        return NULL

    return Integer(value=-evaluated.value)


def evaluate_prefix_expression(node: PrefixExpression):
    match node:
        case PrefixExpression(operator="!"):
            return evaluate_prefix_bang(node)
        case PrefixExpression(operator="-"):
            return evaluate_prefix_minus(node)
        case _:
            return NULL


def evaluate_integer_infix_expression(left: Integer, right: Integer, operator: str):
    match operator:
        case "+":
            return Integer(left.value + right.value)
        case "-":
            return Integer(left.value - right.value)
        case "*":
            return Integer(left.value * right.value)
        case "/":
            if right.value == 0:
                return NULL  # TODO: Should throw error
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


def evaluate(node: Node):
    match node:
        case Program():
            return evaluate_program(node)
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
        case _:
            raise NotImplementedError(f"{type(node)} is still not implemented")

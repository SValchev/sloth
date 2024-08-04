from .ast import (
    BooleanLiteral,
    ExpressionStatement,
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


def evaluate(node: Node):
    match node:
        case Program():
            return evaluate_program(node)
        case ExpressionStatement():
            return evaluate(node.expression)
        case IntegerLiteral():
            return Integer(node.value)
        case BooleanLiteral():
            return TRUE if node.value else FALSE
        case PrefixExpression():
            return evaluate_prefix_expression(node)

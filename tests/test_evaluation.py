from dataclasses import dataclass
from sloth.evaluation import FALSE, TRUE, NULL, evaluate
from sloth.objects import Boolean, Integer, Null
from sloth.parser import Parser


def input_eval(input_: str):
    parser = Parser.from_input(input_)

    program = parser.parse_program()
    return evaluate(program)


def test_integer_eval():
    input = ["5", "10"]
    expected = [5, 10]

    for in_, exp in zip(input, expected):
        evaluated = input_eval(in_)
        assert isinstance(evaluated, Integer)
        assert evaluated.value == exp


def test_boolean_eval():
    @dataclass(frozen=True, slots=True)
    class testing:
        input: str
        expected: bool
        obj: Boolean

    tests = [
        testing("true", True, TRUE),
        testing("false", False, FALSE),
    ]

    for test in tests:
        evaluated = input_eval(test.input)
        assert isinstance(evaluated, Boolean)
        assert evaluated.value == test.expected
        assert evaluated is test.obj


def test_prefix_bool_eval():
    tests = [
        ("!true", FALSE),
        ("!!true", TRUE),
        ("!!!true", FALSE),
        ("!false", TRUE),
        ("!!false", FALSE),
        ("!!!false", TRUE),
        ("!5", FALSE),
        ("!!5", TRUE),
        ("!-5", FALSE),
        ("!!-5", TRUE),
    ]

    for input, expected in tests:
        evaluated = input_eval(input)
        assert isinstance(evaluated, Boolean)
        assert evaluated is expected


def test_prefix_minus_eval():
    tests = [
        ("5", 5),
        ("10", 10),
        ("-10", -10),
        ("-5", -5),
    ]

    for input, expected in tests:
        evaluated = input_eval(input)
        assert isinstance(evaluated, Integer)
        assert evaluated == Integer(expected)


def test_prefix_minus_invalid_eval():
    tests = [
        ("-true", NULL),
        ("-false", NULL),
        ("--true", NULL),
        ("!-false", NULL),
        ("-!false", NULL),
    ]

    for input, expected in tests:
        evaluated = input_eval(input)
        assert evaluated is expected


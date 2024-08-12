from dataclasses import dataclass
from sloth.evaluation import FALSE, TRUE, NULL, Environment, evaluate
from sloth.objects import Boolean, Fault, Integer
from sloth.parser import Parser


def input_eval(input_: str):
    parser = Parser.from_input(input_)

    program = parser.parse_program()
    env = Environment()
    return evaluate(program, env)


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


def test_infix_expression_integer_math_eval():
    tests = [
        ("1 + 1", 2),
        ("1 - 1", 0),
        ("1 * 1", 1),
        ("2 / 2", 1),
        ("(1 + 1) + 1", 3),
        ("1 * 1 + 1", 2),
        ("2 * 2 / 2", 2),
        ("(5 + 5) / 2", 5),
    ]

    for input, expected in tests:
        evaluated = input_eval(input)
        assert evaluated == Integer(expected)


def test_infix_expression_integer_bool_eval():
    tests = [
        ("5 == 5", TRUE),
        ("5 != 5", FALSE),
        ("4 == 5", FALSE),
        ("4 != 5", TRUE),
        ("4 > 5", FALSE),
        ("4 < 5", TRUE),
        ("(4 + 1) != 5", FALSE),
        ("(4 + 1) == 5", TRUE),
    ]
    for input, expected in tests:
        evaluated = input_eval(input)
        assert evaluated == expected


def test_infix_expression_boolean_expression_eval():
    tests = [
        ("true == true", TRUE),
        ("false != false", FALSE),
        ("true == false", FALSE),
        ("true != false", TRUE),
        ("(2 > 1) == true", TRUE),
        ("(2 < 1) == true", FALSE),
        ("(2 < 1) != true", TRUE),
        ("(2 < 1) != false", FALSE),
    ]

    for input, expected in tests:
        evaluated = input_eval(input)
        assert evaluated == expected


def test_if_else_expression_eval():
    tests = [
        ("if(true) {10}", 10),
        ("if(false) {10}", NULL),
        ("if(5 > 2) {10}", 10),
        ("if(5 < 2) {10}", NULL),
        ("if(5 < 2) {10} else {5}", 5),
        ("if(5 > 2) {10} else {5}", 10),
        ("if(5) {10} else {5}", 10),
        # ("if(null) {10} else {5}", 5), # TODO: Can you make null to pass
        ("if(0) {10} else {5}", 5),
        ("if(true) {10} else {5}", 10),
        ("if(false) {10} else {5}", 5),
    ]

    for input, expected in tests:
        evaluated = input_eval(input)
        if isinstance(expected, int):
            expected = Integer(expected)
        print(input)
        assert evaluated == expected


def test_return_eval():
    input = """3 * 3 * 3;
    return 10;
    8 * 8 * 8;
    """

    evaluated = input_eval(input)
    assert evaluated == Integer(10)


def test_nested_return_eval():
    input = """ 
    if (10 > 1) {
        if (10 > 1) {
            return 10;
        }
        return 1;
    }
    """

    evaluated = input_eval(input)
    assert evaluated == Integer(1)


def test_divide_by_zero_fault():
    input = " 2 / 0"

    evaluated = input_eval(input)
    assert isinstance(evaluated, Fault)


def test_var_int_statement_eval():
    tests = [
        ("var x = 5; x;", 5),
        ("var x = 5 + 5; x;", 10),
        ("var x = 5; var y = x; y;", 5),
        ("var x = 5; var y = x + 5; y;", 10),
        ("var x = 5; var y = 5; var z = x + y; z;", 10),
        ("var x = 5; var y = 5; var z = x + 5 + y; z;", 15),
    ]

    for input, expected in tests:
        evaluated = input_eval(input)
        assert evaluated == Integer(expected)


def test_function_calls_int_statement_eval():
    tests = [
        ("var a = func() {return 5}; a()", 5),
        ("var a = 5; var b = 5; var x = func(a, b) {return a + b}; x(a, b);", 10),
        ("var a = 5;  var x = func(a) {return a + 5}; x(a)", 10),
        ("var x = func(a) {return a + 5}; x((2 * 1) + 2 + 1)", 10),
        (
            """
            var a = 5;
            var b = 3;

            var sum = func(a, b) { return a + b };
            var b = 5;
            sum(a, b);
        """,
            10,
        ),
        (
            """
            var a = 5;
            var b = 5;

            var sum = func(a, b) { return a + b };
            var plusFive = func(a) { return a + 5 };

            plusFive(sum(a, b));
        """,
            15,
        ),
    ]

    for input, expected in tests:
        evaluated = input_eval(input)
        assert evaluated == Integer(expected)

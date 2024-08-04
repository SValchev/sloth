from sloth.evaluation import evaluate
from .parser import Parser

from pathlib import Path
import sys
import atexit
import readline


class ExitCommand(Exception):
    pass


class History:
    HISTORY_FILE = Path.home() / ".sloth_history"
    HISTORY_LEN = 100

    @classmethod
    def init(cls):
        cls.load_history()
        atexit.register(cls.save_history)

    @classmethod
    def load_history(cls):
        try:
            readline.read_history_file(cls.HISTORY_FILE)
        except FileNotFoundError:
            pass

    @classmethod
    def save_history(cls):
        """This is not intendend to work on multiple shells at once"""

        prev_h_len = 0
        with cls.HISTORY_FILE.open() as file:
            for _ in file:
                prev_h_len += 1

        new_h_len = readline.get_current_history_length()
        readline.set_history_length(cls.HISTORY_LEN)

        readline.append_history_file(new_h_len - prev_h_len, cls.HISTORY_FILE)


def loop(main):
    def wrapper():
        try:
            while True:
                main()
        except ExitCommand:
            print("Manually interrupted. Will be a slow Goodbye... I'm a sloth")

        sys.exit(0)

    return wrapper


@loop
def relp():
    try:
        input_ = input(">>> ")
    except KeyboardInterrupt:
        sys.stdout.write("\033[2K\033[0G")
        sys.stdout.flush()
        return

    match input_:
        case "exit" | "q" | "exit()":
            raise ExitCommand()
        case _:
            pass

    parser = Parser.from_input(input_)
    program = parser.parse_program()

    if parser.errors:
        errors = "\n".join(map(str, parser.errors))
        print(f"ERRORS: {errors}")
        return

    evaluated = evaluate(program)
    print(evaluated.inspect())


if __name__ == "__main__":
    History.init()
    relp()

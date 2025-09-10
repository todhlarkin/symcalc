import sys
from io import StringIO

import pytest

from symcalc.cli import main


def run_cli(args, input_str: str = "") -> str:
    """Run the CLI with the given arguments and capture stdout."""
    backup_stdout = sys.stdout
    backup_stdin = sys.stdin
    try:
        sys.stdout = StringIO()
        sys.stdin = StringIO(input_str)
        # Execute the CLI
        main(args)
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = backup_stdout
        sys.stdin = backup_stdin


def test_cli_simplify():
    output = run_cli(["simplify", "sin(x)^2 + cos(x)^2"])
    assert output == "1"


def test_cli_diff():
    output = run_cli(["diff", "x^3", "-v", "x", "-o", "2"])
    assert output == "6*x"


def test_cli_integrate():
    output = run_cli(["integrate", "x", "-v", "x", "--a", "0", "--b", "1"])
    assert output == "1/2"


def test_cli_solve():
    output = run_cli(["solve", "x^2 = 9", "-v", "x"])
    # Remove braces and split into individual values
    stripped = output.strip("{}")
    values = {val.strip() for val in stripped.split(",") if val.strip()}
    assert values == {"-3", "3"}


def test_cli_eval_numeric():
    output = run_cli([
        "eval",
        "x*y + 2",
        "--subs",
        "x=3",
        "--subs",
        "y=7",
        "--numeric",
    ])
    # SymPy prints floats with 13 digits by default when pretty-printing
    assert output == "23.0000000000000"

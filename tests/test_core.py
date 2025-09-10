import math
import builtins
import sys

import pytest

from symcalc.core import (
    simplify_expr,
    expand_expr,
    factor_expr,
    diff_expr,
    integrate_expr,
    solve_expr,
    eval_expr,
    latex_expr,
)


def test_simplify():
    # sin^2 + cos^2 should simplify to 1
    assert simplify_expr("sin(x)^2 + cos(x)^2") == 1


def test_expand():
    result = expand_expr("(x+1)^3")
    assert str(result) == "x**3 + 3*x**2 + 3*x + 1"


def test_factor():
    result = factor_expr("x^2 + 2*x + 1")
    # Should factor to (x + 1)**2
    assert str(result) == "(x + 1)**2"


def test_diff():
    result = diff_expr("x^3", var="x", order=2)
    assert str(result) == "6*x"


def test_integrate():
    # Definite integral of x from 0 to 1 is 1/2
    result = integrate_expr("x", var="x", a="0", b="1")
    assert str(result) == "1/2"


def test_solve():
    result = solve_expr("x^2 = 9", var="x")
    # result is a FiniteSet; convert to Python set for comparison
    assert set(result) == {-3, 3}


def test_eval_numeric():
    # Evaluate x*y + 2 with x=3, y=7 -> 23
    result = eval_expr("x*y + 2", substitutions={"x": 3, "y": 7}, numeric=True)
    assert float(result) == 23.0


def test_latex():
    # LaTeX representation should include \sin and \cos
    expr_latex = latex_expr("sin(x)^2 + cos(x)^2")
    assert "\\sin" in expr_latex and "\\cos" in expr_latex

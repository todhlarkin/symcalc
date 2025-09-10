#!/usr/bin/env python
"""Command-line interface for symcalc.

This module provides a CLI for symbolic mathematics using SymPy. It supports
simplification, expansion, factorization, differentiation, integration,
equation solving, evaluation with substitutions, and LaTeX output.
"""
from __future__ import annotations

import argparse
import sys
from typing import Dict, Any

from sympy import pretty

from .core import (
    simplify_expr,
    expand_expr,
    factor_expr,
    diff_expr,
    integrate_expr,
    solve_expr,
    eval_expr,
    latex_expr,
)


def _read_expression(expr_arg: str | None) -> str:
    """Return an expression string from an argument or standard input."""
    if expr_arg is not None:
        return expr_arg
    # Read entire stdin
    data = sys.stdin.read().strip()
    if not data:
        raise SystemExit("No expression provided")
    return data


def _format_result(result: Any, ascii_output: bool = False, latex_out: bool = False) -> str:
    """Format the result for output based on flags.

    If latex_out is True, return a LaTeX string. Otherwise pretty-print the
    expression using SymPy. When ascii_output is True, use ASCII characters.
    """
    if latex_out:
        # If result is already a string (e.g. latex subcommand), return it directly
        return result if isinstance(result, str) else latex_expr(str(result))
    return pretty(result, use_unicode=not ascii_output)


def handle_simplify(args: argparse.Namespace) -> None:
    expr_str = _read_expression(args.expr)
    result = simplify_expr(expr_str)
    ascii_output = args.ascii and not args.unicode
    output = _format_result(result, ascii_output=ascii_output, latex_out=args.latex_out)
    print(output)


def handle_expand(args: argparse.Namespace) -> None:
    expr_str = _read_expression(args.expr)
    result = expand_expr(expr_str)
    ascii_output = args.ascii and not args.unicode
    output = _format_result(result, ascii_output=ascii_output, latex_out=args.latex_out)
    print(output)


def handle_factor(args: argparse.Namespace) -> None:
    expr_str = _read_expression(args.expr)
    result = factor_expr(expr_str)
    ascii_output = args.ascii and not args.unicode
    output = _format_result(result, ascii_output=ascii_output, latex_out=args.latex_out)
    print(output)


def handle_diff(args: argparse.Namespace) -> None:
    expr_str = _read_expression(args.expr)
    result = diff_expr(expr_str, var=args.var, order=args.order)
    ascii_output = args.ascii and not args.unicode
    output = _format_result(result, ascii_output=ascii_output, latex_out=args.latex_out)
    print(output)


def handle_integrate(args: argparse.Namespace) -> None:
    expr_str = _read_expression(args.expr)
    result = integrate_expr(expr_str, var=args.var, a=args.a, b=args.b)
    ascii_output = args.ascii and not args.unicode
    output = _format_result(result, ascii_output=ascii_output, latex_out=args.latex_out)
    print(output)


def handle_solve(args: argparse.Namespace) -> None:
    expr_str = _read_expression(args.expr)
    result = solve_expr(expr_str, var=args.var)
    ascii_output = args.ascii and not args.unicode
    output = _format_result(result, ascii_output=ascii_output, latex_out=args.latex_out)
    print(output)


def handle_eval(args: argparse.Namespace) -> None:
    expr_str = _read_expression(args.expr)
    subs_dict: Dict[str, Any] = {}
    if args.subs:
        for sub in args.subs:
            if "=" not in sub:
                raise SystemExit(f"Invalid substitution format: {sub}. Use var=value.")
            name, value = sub.split("=", 1)
            subs_dict[name] = value
    result = eval_expr(expr_str, substitutions=subs_dict, numeric=args.numeric)
    ascii_output = args.ascii and not args.unicode
    output = _format_result(result, ascii_output=ascii_output, latex_out=args.latex_out)
    print(output)


def handle_latex(args: argparse.Namespace) -> None:
    expr_str = _read_expression(args.expr)
    # Directly generate LaTeX output for this subcommand
    result = latex_expr(expr_str)
    print(result)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="symcalc",
        description="symcalc: command-line symbolic mathematics powered by SymPy",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Global flags for output formatting
    parser.add_argument(
        "--ascii", action="store_true", help="use ASCII characters in output"
    )
    parser.add_argument(
        "--unicode",
        action="store_true",
        help="use Unicode characters in output (default)",
    )
    parser.add_argument(
        "--latex-out", action="store_true", help="output result in LaTeX form"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # simplify
    parser_simplify = subparsers.add_parser(
        "simplify", help="Simplify an expression"
    )
    parser_simplify.add_argument(
        "expr", nargs="?", help="expression to simplify"
    )
    parser_simplify.set_defaults(func=handle_simplify)

    # expand
    parser_expand = subparsers.add_parser(
        "expand", help="Expand products and powers in an expression"
    )
    parser_expand.add_argument(
        "expr", nargs="?", help="expression to expand"
    )
    parser_expand.set_defaults(func=handle_expand)

    # factor
    parser_factor = subparsers.add_parser(
        "factor", help="Factor an expression"
    )
    parser_factor.add_argument("expr", nargs="?", help="expression to factor")
    parser_factor.set_defaults(func=handle_factor)

    # diff
    parser_diff_cmd = subparsers.add_parser(
        "diff", help="Differentiate an expression"
    )
    parser_diff_cmd.add_argument("expr", nargs="?", help="expression to differentiate")
    parser_diff_cmd.add_argument(
        "-v",
        "--var",
        help="variable to differentiate with respect to (defaults to first free symbol)",
    )
    parser_diff_cmd.add_argument(
        "-o",
        "--order",
        type=int,
        default=1,
        help="order of the derivative",
    )
    parser_diff_cmd.set_defaults(func=handle_diff)

    # integrate
    parser_integrate = subparsers.add_parser(
        "integrate", help="Integrate an expression"
    )
    parser_integrate.add_argument(
        "expr", nargs="?", help="expression to integrate"
    )
    parser_integrate.add_argument(
        "-v",
        "--var",
        help="variable to integrate with respect to (defaults to first free symbol)",
    )
    parser_integrate.add_argument(
        "--a",
        help="lower limit of integration (for definite integrals)",
    )
    parser_integrate.add_argument(
        "--b",
        help="upper limit of integration (for definite integrals)",
    )
    parser_integrate.set_defaults(func=handle_integrate)

    # solve
    parser_solve = subparsers.add_parser(
        "solve", help="Solve an equation or expression equal to zero"
    )
    parser_solve.add_argument(
        "expr",
        nargs="?",
        help="equation of the form 'expr = rhs' or just an expression",
    )
    parser_solve.add_argument(
        "-v",
        "--var",
        help="variable to solve for (defaults to first free symbol)",
    )
    parser_solve.set_defaults(func=handle_solve)

    # eval
    parser_eval = subparsers.add_parser(
        "eval", help="Evaluate an expression with optional substitutions"
    )
    parser_eval.add_argument(
        "expr", nargs="?", help="expression to evaluate"
    )
    parser_eval.add_argument(
        "--subs",
        action="append",
        help="substitution in the form var=value (can be specified multiple times)",
    )
    parser_eval.add_argument(
        "--numeric",
        action="store_true",
        help="evaluate the result to a floating-point number",
    )
    parser_eval.set_defaults(func=handle_eval)

    # latex
    parser_latex = subparsers.add_parser(
        "latex", help="Output the LaTeX representation of an expression"
    )
    parser_latex.add_argument(
        "expr", nargs="?", help="expression to convert to LaTeX"
    )
    parser_latex.set_defaults(func=handle_latex)

    args = parser.parse_args(argv)
    # Call the appropriate handler function
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()

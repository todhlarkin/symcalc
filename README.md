# symcalc

`symcalc` is a command-line tool for symbolic mathematics built on top of [SymPy](https://www.sympy.org/).

## Features

- Simplify algebraic expressions
- Expand products and powers
- Factor expressions
- Differentiate expressions of arbitrary order
- Integrate expressions symbolically and compute definite integrals
- Solve algebraic equations
- Substitute values and evaluate expressions numerically
- Output expressions in Unicode, ASCII, or LaTeX format

## Installation

Requires Python 3.8 or newer.

```bash
pip install symcalc
```

Alternatively, clone this repository and install from source:

```bash
git clone https://github.com/<your-username>/symcalc.git
cd symcalc
pip install .
```

## Usage

## Quick Start

Here are some common operations you can perform with `symcalc`:

- **Simplify an algebraic expression:**

  ```bash
  symcalc simplify "2*x + 3*x - 5"
  # Output: 5*x - 5
  ```

- **Expand a product:**

  ```bash
  symcalc expand "(x + 2)*(x - 2)"
  # Output: x**2 - 4
  ```

- **Factor an expression:**

  ```bash
  symcalc factor "x**2 - 5*x + 6"
  # Output: (x - 2)*(x - 3)
  ```

- **Differentiate an expression:**

  ```bash
  symcalc diff "sin(x)" x
  # Output: cos(x)
  ```

- **Integrate an expression:**

  ```bash
  symcalc integrate "x**2" x
  # Output: x**3/3
  ```

- **Evaluate an expression numerically:**

  ```bash
  symcalc eval "x**2 + y**2" --subs x=3 --subs y=4 --numeric
  # Output: 25
  ```

Run `symcalc --help` to see all available commands and options.

Use the `symcalc` command followed by a subcommand and an expression:

```bash
# Simplify an expression
symcalc simplify "sin(x)^2 + cos(x)^2"

# Expand a product
symcalc expand "(x + 1)^3"

# Differentiate an expression
symcalc diff "x^3" -v x -o 2

# Integrate an expression
symcalc integrate "x" -v x --a 0 --b 1

# Solve an equation
symcalc solve "x^2 - 4" -v x

# Substitute values and evaluate
symcalc eval "x*y + 2" --subs x=3 --subs y=7 --numeric

# Output LaTeX
symcalc latex "sin(x)^2 + cos(x)^2"
```

Run `symcalc --help` for more details on available commands and options.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

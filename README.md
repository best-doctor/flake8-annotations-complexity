# flake8-annotations-complexity

[![Build Status](https://github.com/best-doctor/flake8-annotations-complexity/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/best-doctor/flake8-annotations-complexity/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/flake8-annotations-complexity.svg)](https://badge.fury.io/py/flake8-annotations-complexity)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-annotations-complexity)

An extension for flake8 to report on too complex type annotations.

Complex type annotations often means bad annotations usage,
wrong code decomposition or improper data structure choice.
They are also hard to read and make code look java-like.

Annotation complexity is maximum annotation nesting level.
So `List[int]` complexity is 2 and `Tuple[List[Optional[str]], int]` is 4.

The plugin checks annotations of every argument kind (positional-only, regular,
`*args`, keyword-only and `**kwargs`), return types of both regular and `async`
functions, and annotated assignments.

## Checks

| Code | Description | Option | Default |
| --- | --- | --- | --- |
| `TAE002` | Annotation is too complex (nesting level) | `--max-annotations-complexity` | 3 |
| `TAE003` | Annotation is too long (number of elements) | `--max-annotations-len` | 7 |

## Requirements

Python 3.10 – 3.14.

## Installation

```bash
pip install flake8-annotations-complexity
```

## Example

Sample file:

```python
# test.py


def foo() -> List[int]:
    return [1]
```

Usage:

```terminal
$ flake8 --max-annotations-complexity=1 test.py
test.py:4:14: TAE002 too complex annotation (2 > 1)
```

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

- The project uses [uv](https://docs.astral.sh/uv/). Run `make install` (or `uv sync`)
  to create the environment.
- Install the git hooks once with `uv run pre-commit install`.
- You can run all checks and tests with `make check`.
  Please do it before CI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.

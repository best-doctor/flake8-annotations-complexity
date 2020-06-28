# flake8-annotations-complexity

[![Build Status](https://travis-ci.org/best-doctor/flake8-annotations-complexity.svg?branch=master)](https://travis-ci.org/best-doctor/flake8-annotations-complexity)
[![Maintainability](https://api.codeclimate.com/v1/badges/c81ff76755380663b7d3/maintainability)](https://codeclimate.com/github/best-doctor/flake8-annotations-complexity/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c81ff76755380663b7d3/test_coverage)](https://codeclimate.com/github/best-doctor/flake8-annotations-complexity/test_coverage)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-annotations-complexity)

An extension for flake8 to report on too complex type annotations.

Complex type annotations often means bad annotations usage,
wrong code decomposition or improper data structure choice.
They are also hard to read and make code look java-like.

Annotation complexity is maximum annotation nesting level.
So `List[int]` complexity is 2 and `Tuple[List[Optional[str]], int]` is 4.

Default max annotation complexity is 3 and can be configured
via `--max-annotations-complexity` option.

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

Tested on Python 3.5.0 and flake8 3.7.4.

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`.
  Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.

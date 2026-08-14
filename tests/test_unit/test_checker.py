import argparse

import pytest

from flake8_annotations_complexity.checker import AnnotationsComplexityChecker


class FakeOptionParser:
    def __init__(self) -> None:
        self.options: dict = {}

    def add_option(self, name: str, **kwargs) -> None:
        self.options[name] = kwargs


@pytest.mark.parametrize(
    ('filename', 'max_complexity'),
    [
        ('empty.py', None),
        ('empty.py', 1),
        ('unannotated.py', 1),
        ('weird_annotations.py', None),
        ('pep_585.py', None),
        ('empty_tuple.py', 2),
        ('empty_string.py', 2),
    ],
    ids=[
        'empty-file-default',
        'empty-file-strict',
        'unannotated-file',
        'weird-annotations',
        'pep-585-builtins',
        'empty-tuple',
        'empty-string',
    ],
)
def test__run__no_errors_for_simple_annotations(run_validator, filename, max_complexity):
    """
    Arrange: a file with no annotation exceeding the limit.
    Act: run the checker over the file.
    Assert: no errors are reported.
    """
    errors = run_validator(filename, max_annotations_complexity=max_complexity)

    assert not errors


@pytest.mark.parametrize(
    ('filename', 'max_complexity', 'expected_errors_count'),
    [
        ('dynamic_annotations.py', None, 1),
        ('dynamic_annotations.py', 2, 1),
        ('dynamic_annotations.py', 1, 3),
        ('string_annotations.py', None, 1),
        ('string_annotations.py', 1, 2),
        ('var_annotation.py', None, 1),
        ('empty_tuple.py', 1, 1),
        ('empty_string.py', 1, 2),
        ('pep_585.py', 1, 11),
        ('pep_585.py', 2, 2),
    ],
    ids=[
        'dynamic-default',
        'dynamic-limit-2',
        'dynamic-limit-1',
        'string-default',
        'string-limit-1',
        'annotated-assignment',
        'empty-tuple-limit-1',
        'empty-string-limit-1',
        'pep-585-limit-1',
        'pep-585-limit-2',
    ],
)
def test__run__reports_too_complex_annotations(
    run_validator,
    filename,
    max_complexity,
    expected_errors_count,
):
    """
    Arrange: a file with annotations and a given complexity limit.
    Act: run the checker over the file.
    Assert: the number of reported errors matches the expectation.
    """
    errors = run_validator(filename, max_annotations_complexity=max_complexity)

    assert len(errors) == expected_errors_count


@pytest.mark.parametrize(
    ('filename', 'max_len', 'expected_errors_count'),
    [
        ('too_long_annotation.py', None, 4),
        ('too_long_annotation.py', 8, 3),
        ('async_too_long_annotation.py', None, 1),
        ('async_too_long_annotation.py', 9, 0),
    ],
    ids=['default-limit', 'limit-8', 'async-default-limit', 'async-limit-9'],
)
def test__run__reports_too_long_annotations(
    run_validator,
    filename,
    max_len,
    expected_errors_count,
):
    """
    Arrange: a file with long annotations and a given length limit.
    Act: run the checker over the file.
    Assert: the length limit is honoured and the error count matches.
    """
    errors = run_validator(filename, max_annotations_len=max_len)

    assert len(errors) == expected_errors_count


@pytest.mark.parametrize(
    ('filename', 'max_complexity', 'expected_errors_count'),
    [
        ('async_annotations.py', None, 1),
        ('async_annotations.py', 1, 2),
        ('async_string_annotations.py', None, 1),
        ('async_string_annotations.py', 1, 2),
        ('async_nested.py', None, 4),
        ('async_nested.py', 5, 1),
    ],
    ids=[
        'async-default',
        'async-limit-1',
        'async-string-default',
        'async-string-limit-1',
        'async-nested-default',
        'async-nested-limit-5',
    ],
)
def test__run__checks_async_functions(
    run_validator,
    filename,
    max_complexity,
    expected_errors_count,
):
    """
    Arrange: a file with async functions, methods, nested defs and generators.
    Act: run the checker over the file.
    Assert: async annotations are checked just like synchronous ones.
    """
    errors = run_validator(filename, max_annotations_complexity=max_complexity)

    assert len(errors) == expected_errors_count


@pytest.mark.parametrize(
    'filename',
    ['all_arg_kinds.py', 'async_arg_kinds.py'],
    ids=['sync', 'async'],
)
def test__run__checks_all_argument_kinds(run_validator, filename):
    """
    Arrange: a function with every argument kind, each annotated too deeply.
    Act: run the checker over the file.
    Assert: an error is reported for all five argument kinds.
    """
    errors = run_validator(filename)

    assert len(errors) == 5


@pytest.mark.parametrize(
    ('filename', 'expected_code'),
    [
        ('all_arg_kinds.py', 'TAE002'),
        ('async_too_long_annotation.py', 'TAE003'),
    ],
    ids=['too-complex', 'too-long'],
)
def test__run__reports_expected_error_code(run_validator, filename, expected_code):
    """
    Arrange: a file violating exactly one of the checks.
    Act: run the checker over the file.
    Assert: every message starts with the expected error code.
    """
    errors = run_validator(filename)

    assert all(message.startswith(expected_code) for _, _, message, _ in errors)


def test__run__reports_annotation_position(run_validator):
    """
    Arrange: a file with a single too complex annotation at a known position.
    Act: run the checker over the file.
    Assert: the error points at the line and column of the annotation.
    """
    errors = run_validator('var_annotation.py')

    line, col, _, checker_type = errors[0]
    assert (line, col) == (2, 5)
    assert checker_type is AnnotationsComplexityChecker


def test__add_options__registers_both_options():
    """
    Arrange: a fake flake8 option parser.
    Act: register the checker options.
    Assert: both options are registered with their default values.
    """
    parser = FakeOptionParser()

    AnnotationsComplexityChecker.add_options(parser)

    assert set(parser.options) == {'--max-annotations-complexity', '--max-annotations-len'}
    assert parser.options['--max-annotations-complexity']['default'] == 3
    assert parser.options['--max-annotations-len']['default'] == 7


@pytest.mark.usefixtures('restore_checker_limits')
def test__parse_options__applies_both_limits():
    """
    Arrange: parsed flake8 options carrying both limits.
    Act: apply the options to the checker.
    Assert: both limits are applied, not only the complexity one.
    """
    options = argparse.Namespace(max_annotations_complexity=5, max_annotations_len=9)

    AnnotationsComplexityChecker.parse_options(options)

    assert AnnotationsComplexityChecker.max_annotations_complexity == 5
    assert AnnotationsComplexityChecker.max_annotations_len == 9

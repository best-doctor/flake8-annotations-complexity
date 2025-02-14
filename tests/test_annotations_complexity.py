import sys

import pytest

from conftest import run_validator_for_test_file


def test_always_ok_for_empty_file():
    errors = run_validator_for_test_file('empty.py')
    assert not errors
    errors = run_validator_for_test_file('empty.py', max_annotations_complexity=1)
    assert not errors


def test_ok_for_unannotated_file():
    errors = run_validator_for_test_file('unannotated.py', max_annotations_complexity=1)
    assert not errors


def test_ok_for_dynamic_annotations_file():
    errors = run_validator_for_test_file('dynamic_annotations.py')
    assert len(errors) == 1
    errors = run_validator_for_test_file('dynamic_annotations.py', max_annotations_complexity=2)
    assert len(errors) == 1
    errors = run_validator_for_test_file('dynamic_annotations.py', max_annotations_complexity=1)
    assert len(errors) == 3


def test_ok_for_string_annotations_file():
    errors = run_validator_for_test_file('string_annotations.py')
    assert len(errors) == 1
    errors = run_validator_for_test_file('string_annotations.py', max_annotations_complexity=1)
    assert len(errors) == 2


def test_validates_annotations_complexity_for_annassigments():
    errors = run_validator_for_test_file('var_annotation.py')
    assert len(errors) == 1


def test_ok_for_empty_tuple():
    errors = run_validator_for_test_file('empty_tuple.py')
    assert not errors
    errors = run_validator_for_test_file('empty_tuple.py', max_annotations_complexity=1)
    assert len(errors) == 1
    errors = run_validator_for_test_file('empty_tuple.py', max_annotations_complexity=2)
    assert not errors


def test_not_raises_errors_for_weird_annotations():
    errors = run_validator_for_test_file('weird_annotations.py')
    assert not errors


def test_ok_for_empty_string():
    errors = run_validator_for_test_file('empty_string.py')
    assert not errors
    errors = run_validator_for_test_file('empty_string.py', max_annotations_complexity=1)
    assert len(errors) == 2
    errors = run_validator_for_test_file('empty_string.py', max_annotations_complexity=2)
    assert not errors


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires Python 3.7+")
def test_pep_585_compliance():
    errors = run_validator_for_test_file('pep_585.py')
    assert not errors
    errors = run_validator_for_test_file('pep_585.py', max_annotations_complexity=1)
    assert len(errors) == 11
    errors = run_validator_for_test_file('pep_585.py', max_annotations_complexity=2)
    assert len(errors) == 2


def test_validates_too_long_annotations():
    errors = run_validator_for_test_file('too_long_annotation.py')
    assert len(errors) == 4

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
    errors = run_validator_for_test_file('dynamic_annotations.py', max_annotations_complexity=1)
    assert len(errors) == 2


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
    assert not errors

import ast
import os

from flake8_annotations_complexity.checker import AnnotationsChecker


def run_validator_for_test_file(filename, max_annotations_complexity=None):
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_files',
        filename,
    )
    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)
    checker = AnnotationsChecker(tree=tree, filename=filename)
    if max_annotations_complexity:
        checker.max_annotations_complexity = max_annotations_complexity

    return list(checker.run())

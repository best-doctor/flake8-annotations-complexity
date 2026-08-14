import ast
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from flake8_annotations_complexity.checker import AnnotationsComplexityChecker

TEST_FILES_DIR = Path(__file__).resolve().parent / 'test_files'

CheckerErrors = list[tuple[int, int, str, type]]


@pytest.fixture()
def run_validator() -> Callable[..., CheckerErrors]:
    def _run_validator(
        filename: str,
        max_annotations_complexity: int | None = None,
        max_annotations_len: int | None = None,
    ) -> CheckerErrors:
        tree = ast.parse((TEST_FILES_DIR / filename).read_text())
        checker = AnnotationsComplexityChecker(tree=tree, filename=filename)
        if max_annotations_complexity:
            checker.max_annotations_complexity = max_annotations_complexity
        if max_annotations_len:
            checker.max_annotations_len = max_annotations_len

        return list(checker.run())

    return _run_validator


@pytest.fixture()
def restore_checker_limits() -> Iterator[None]:
    complexity = AnnotationsComplexityChecker.max_annotations_complexity
    length = AnnotationsComplexityChecker.max_annotations_len

    yield

    AnnotationsComplexityChecker.max_annotations_complexity = complexity
    AnnotationsComplexityChecker.max_annotations_len = length

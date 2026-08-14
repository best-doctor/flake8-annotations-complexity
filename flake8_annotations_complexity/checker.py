import ast
from collections.abc import Iterator
from typing import Any

from flake8_annotations_complexity import __version__ as version
from flake8_annotations_complexity.ast_helpers import validate_annotations_in_ast_node


class AnnotationsComplexityChecker:
    name = 'flake8-annotations-complexity'
    version = version

    default_max_annotations_complexity = 3
    default_max_annotations_len = 7

    # Overwritten by ``parse_options`` when flake8 drives the checker.
    max_annotations_complexity: int = default_max_annotations_complexity
    max_annotations_len: int = default_max_annotations_len

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self.filename = filename
        self.tree = tree

    @classmethod
    def add_options(cls, parser: Any) -> None:
        parser.add_option(
            '--max-annotations-complexity',
            type=int,
            parse_from_config=True,
            default=cls.default_max_annotations_complexity,
        )
        parser.add_option(
            '--max-annotations-len',
            type=int,
            parse_from_config=True,
            default=cls.default_max_annotations_len,
        )

    @classmethod
    def parse_options(cls, options: Any) -> None:
        cls.max_annotations_complexity = int(options.max_annotations_complexity)
        cls.max_annotations_len = int(options.max_annotations_len)

    def run(self) -> Iterator[tuple[int, int, str, type]]:
        too_difficult_annotations = validate_annotations_in_ast_node(
            self.tree,
            self.max_annotations_complexity,
            self.max_annotations_len,
        )

        for annotation, error_msg in too_difficult_annotations:
            yield (
                annotation.lineno,
                annotation.col_offset,
                error_msg,
                type(self),
            )

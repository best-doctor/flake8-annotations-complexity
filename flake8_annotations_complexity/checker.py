from typing import Generator, Tuple

from flake8_annotations_complexity import __version__ as version
from flake8_annotations_complexity.ast_helpers import validate_annotations_in_ast_node


class AnnotationsComplexityChecker:
    name = 'flake8-annotations-complexity'
    version = version

    max_annotations_complexity = None
    default_max_annotations_complexity = 3

    max_annotations_len = None
    default_max_annotations_len = 7

    def __init__(self, tree, filename: str):
        self.filename = filename
        self.tree = tree
        if AnnotationsComplexityChecker.max_annotations_complexity is None:
            AnnotationsComplexityChecker.max_annotations_complexity = self.default_max_annotations_complexity
        if AnnotationsComplexityChecker.max_annotations_len is None:
            AnnotationsComplexityChecker.max_annotations_len = self.default_max_annotations_len

    @classmethod
    def add_options(cls, parser) -> None:
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
    def parse_options(cls, options) -> None:
        cls.max_annotations_complexity = int(options.max_annotations_complexity)

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
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

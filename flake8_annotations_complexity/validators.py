import abc
import ast
import sys
from typing import Optional


class Validator(abc.ABC):
    """Abstract interface for any validator."""

    @property
    @abc.abstractmethod
    def error_template(self) -> str:
        """Getter for error_template."""

    @abc.abstractmethod
    def validate(self, annotation_node) -> Optional[str]:
        """Check a annotation ast node."""


class AnnotationComplexity(Validator):
    """Validator for check annotation complexity."""

    error_template: str = 'TAE002 too complex annotation ({0} > {1})'

    def __init__(self, max_complexity: int):
        self.max_complexity: int = max_complexity

    def validate(self, annotation_node) -> Optional[str]:
        complexity = self.get_annotation_complexity(annotation_node)
        if complexity <= self.max_complexity:
            return None
        return self.error_template.format(complexity, self.max_complexity)

    def get_annotation_complexity(self, annotation_node, default_complexity: int = 1) -> int:
        if isinstance(annotation_node, ast.Str):
            try:
                annotation_node = ast.parse(annotation_node.s).body[0].value  # type: ignore
            except (SyntaxError, IndexError):
                return default_complexity
        if isinstance(annotation_node, ast.Subscript):
            if sys.version_info >= (3, 9):
                return 1 + self.get_annotation_complexity(annotation_node.slice)
            return 1 + self.get_annotation_complexity(annotation_node.slice.value)  # type: ignore
        if isinstance(annotation_node, ast.Tuple):
            return max((self.get_annotation_complexity(n) for n in annotation_node.elts), default=1)
        return default_complexity


class AnnotationLength(Validator):
    """Validator for check annotation length."""

    error_template: str = 'TAE003 too long annotation ({0} > {1})'

    def __init__(self, max_length: int):
        self.max_length = max_length

    def validate(self, annotation_node) -> Optional[str]:
        annotation_length: int = self.get_annotation_length(annotation_node)
        if annotation_length < self.max_length:
            return None
        return self.error_template.format(annotation_length, self.max_length)

    def get_annotation_length(self, annotation_node) -> int:
        default_len: int = 0
        if isinstance(annotation_node, ast.Str):
            try:
                annotation_node = ast.parse(annotation_node.s).body[0].value  # type: ignore
            except (SyntaxError, IndexError):
                return default_len
        if isinstance(annotation_node, ast.Subscript):
            try:
                if sys.version_info >= (3, 9):
                    return len(annotation_node.slice.elts)  # type: ignore
                return len(annotation_node.slice.value.elts)  # type: ignore
            except AttributeError:
                return default_len
        return default_len

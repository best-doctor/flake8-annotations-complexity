import ast

import pytest

from flake8_annotations_complexity.ast_helpers import get_annotation_complexity, get_annotation_len


def parse_annotation(source: str) -> ast.expr:
    return ast.parse(f'x: {source}').body[0].annotation


@pytest.mark.parametrize(
    ('annotation', 'expected_complexity'),
    [
        ('int', 1),
        ('List[int]', 2),
        ('Tuple[List[Optional[str]], int]', 4),
        ('Tuple[List[Optional[Dict[str, int]]], int]', 5),
        ('dict[str, list[int]]', 3),
    ],
    ids=[
        'plain-name',
        'single-nesting',
        'readme-example',
        'deep-nesting',
        'pep-585-builtin',
    ],
)
def test__get_annotation_complexity__counts_nesting_level(annotation, expected_complexity):
    """
    Arrange: an annotation with a known nesting level.
    Act: count its complexity.
    Assert: complexity equals the deepest nesting level.
    """
    node = parse_annotation(annotation)

    complexity = get_annotation_complexity(node)

    assert complexity == expected_complexity


@pytest.mark.parametrize(
    ('annotation', 'expected_complexity'),
    [
        ("'List[int]'", 2),
        ("'Tuple[List[Optional[Dict[str, int]]], int]'", 5),
        ("'int'", 1),
    ],
    ids=['single-nesting', 'deep-nesting', 'plain-name'],
)
def test__get_annotation_complexity__unwraps_string_annotations(annotation, expected_complexity):
    """
    Arrange: an annotation wrapped in a string literal.
    Act: count its complexity.
    Assert: the string is parsed and complexity matches the unwrapped form.
    """
    node = parse_annotation(annotation)

    complexity = get_annotation_complexity(node)

    assert complexity == expected_complexity


@pytest.mark.parametrize(
    ('annotation', 'expected_complexity'),
    [
        ('Tuple[()]', 2),
        ("Literal['']", 2),
        ("'String Annotation'", 1),
        ('None', 1),
    ],
    ids=['empty-tuple', 'empty-string', 'unparseable-string', 'none'],
)
def test__get_annotation_complexity__degenerate_annotations(annotation, expected_complexity):
    """
    Arrange: a degenerate annotation that is empty or cannot be parsed.
    Act: count its complexity.
    Assert: nothing is raised and a safe fallback value is returned.
    """
    node = parse_annotation(annotation)

    complexity = get_annotation_complexity(node)

    assert complexity == expected_complexity


@pytest.mark.parametrize(
    ('annotation', 'expected_len'),
    [
        ('int', 0),
        ('List[int]', 0),
        ('Tuple[str, int]', 2),
        ('Tuple[str, str, str, int, List, Any, str, Dict, int]', 9),
        ('Foo[[a, b, c]]', 3),
        ('Callable[[int, str], None]', 2),
        ("'Tuple[str, int]'", 2),
        ("'String Annotation'", 0),
    ],
    ids=[
        'plain-name',
        'non-tuple-subscript',
        'two-elements',
        'nine-elements',
        'list-slice',
        'callable-signature',
        'string-wrapped',
        'unparseable-string',
    ],
)
def test__get_annotation_len__counts_subscript_elements(annotation, expected_len):
    """
    Arrange: an annotation with a known number of subscript elements.
    Act: count its length.
    Assert: length equals the number of elements in the subscript.
    """
    node = parse_annotation(annotation)

    annotation_len = get_annotation_len(node)

    assert annotation_len == expected_len

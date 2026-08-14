import ast
from collections.abc import Iterator
from logging import getLogger
from typing import Any

logger = getLogger(__name__)


def _unwrap_annotation(annotation_node: ast.AST) -> ast.AST | None:
    """
    Return the node to analyse, parsing string-wrapped annotations along the way.

    Returns ``None`` if a string annotation cannot be parsed.
    """
    if not (isinstance(annotation_node, ast.Constant) and isinstance(annotation_node.value, str)):
        return annotation_node
    try:
        return ast.parse(annotation_node.value).body[0].value  # type: ignore[attr-defined]
    except Exception as exc:
        # PEP 3107 allows arbitrary expressions in annotations, so a string
        # annotation is not guaranteed to be parseable at all.
        logger.debug(f'Cannot parse string-wrapped annotation: {exc!r}')
        return None


def get_annotation_complexity(annotation_node: ast.AST) -> int:
    """
    Recursively counts complexity of annotation nodes.

    When annotations are written as strings,
    we additionally parse them to ``ast`` nodes.
    """
    unwrapped = _unwrap_annotation(annotation_node)
    if unwrapped is None:
        return 1
    annotation_node = unwrapped

    if isinstance(annotation_node, ast.Subscript):
        return 1 + get_annotation_complexity(annotation_node.slice)

    if isinstance(annotation_node, (ast.Tuple, ast.List)):
        return max((get_annotation_complexity(n) for n in annotation_node.elts), default=1)

    return 1


def get_annotation_len(annotation_node: ast.AST) -> int:
    """
    Recursively counts length of annotation nodes.

    When annotations are written as strings,
    we additionally parse them to ``ast`` nodes.
    """
    unwrapped = _unwrap_annotation(annotation_node)
    if unwrapped is None:
        return 0
    annotation_node = unwrapped

    if isinstance(annotation_node, ast.Subscript) and isinstance(
        annotation_node.slice, (ast.Tuple, ast.List)
    ):
        return len(annotation_node.slice.elts)

    return 0


def _iter_func_annotations(funcdef: ast.FunctionDef | ast.AsyncFunctionDef) -> Iterator[ast.expr]:
    """Yield every annotation of a function: all argument kinds and the return type."""
    args = funcdef.args
    all_args = [
        *args.posonlyargs,
        *args.args,
        *args.kwonlyargs,
        *(arg for arg in (args.vararg, args.kwarg) if arg is not None),
    ]
    for arg in all_args:
        if arg.annotation:
            yield arg.annotation
    if funcdef.returns:
        yield funcdef.returns


def validate_annotations_in_ast_node(
    node: ast.AST,
    max_annotations_complexity: int,
    max_annotations_len: int,
) -> list[tuple[Any, str]]:
    too_difficult_annotations = []
    annotations: list[ast.expr] = []
    for child in ast.walk(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            annotations += _iter_func_annotations(child)
        elif isinstance(child, ast.AnnAssign) and child.annotation:
            annotations.append(child.annotation)

    for annotation in annotations:
        complexity = get_annotation_complexity(annotation)
        if complexity > max_annotations_complexity:
            too_difficult_annotations.append(
                (
                    annotation,
                    f'TAE002 too complex annotation ({complexity} > {max_annotations_complexity})',
                )
            )
        annotation_len = get_annotation_len(annotation)
        if annotation_len > max_annotations_len:
            too_difficult_annotations.append(
                (
                    annotation,
                    f'TAE003 too long annotation ({annotation_len} > {max_annotations_len})',
                )
            )
    return too_difficult_annotations

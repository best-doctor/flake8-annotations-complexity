import ast
import sys
from typing import List, Tuple, Any


def get_annotation_complexity(annotation_node, default_complexity: int = 1) -> int:
    if isinstance(annotation_node, ast.Str):
        try:
            annotation_node = ast.parse(annotation_node.s).body[0].value  # type: ignore
        except (SyntaxError, IndexError):
            return default_complexity
    complexity = default_complexity
    if isinstance(annotation_node, ast.Subscript):
        if sys.version_info >= (3, 9):
            complexity = 1 + get_annotation_complexity(annotation_node.slice)
        else:
            complexity = 1 + get_annotation_complexity(annotation_node.slice.value)  # type: ignore
    if isinstance(annotation_node, ast.Tuple):
        complexity = max((get_annotation_complexity(n) for n in annotation_node.elts), default=1)
    return complexity


def get_annotation_len(annotation_node) -> int:
    annotation_len = 0
    if isinstance(annotation_node, ast.Str):
        try:
            annotation_node = ast.parse(annotation_node.s).body[0].value  # type: ignore
        except (SyntaxError, IndexError):
            return annotation_len
    if isinstance(annotation_node, ast.Subscript):
        try:
            if sys.version_info >= (3, 9):
                annotation_len = len(annotation_node.slice.elts)  # type: ignore
            else:
                annotation_len = len(annotation_node.slice.value.elts)  # type: ignore
        except AttributeError:
            annotation_len = 0
    return annotation_len


def validate_annotations_in_ast_node(
    node,
    max_annotations_complexity,
    max_annotations_len,
) -> List[Tuple[Any, str]]:
    too_difficult_annotations = []
    func_defs = [
        f for f in ast.walk(node)
        if isinstance(f, ast.FunctionDef)
    ]
    annotations: List[ast.AST] = []
    for funcdef in func_defs:
        annotations += list(filter(None, (a.annotation for a in funcdef.args.args)))
        if funcdef.returns:
            annotations.append(funcdef.returns)
    annotations += [a.annotation for a in ast.walk(node) if isinstance(a, ast.AnnAssign) and a.annotation]
    for annotation in annotations:
        complexity = get_annotation_complexity(annotation)
        if complexity > max_annotations_complexity:
            too_difficult_annotations.append((
                annotation,
                'TAE002 too complex annotation ({0} > {1})'.format(complexity, max_annotations_complexity),
            ))
        annotation_len = get_annotation_len(annotation)
        if annotation_len > max_annotations_len:
            too_difficult_annotations.append((
                annotation,
                'TAE003 too long annotation ({0} > {1})'.format(annotation_len, max_annotations_len),
            ))
    return too_difficult_annotations

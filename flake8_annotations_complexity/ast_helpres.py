import ast
from typing import List, Tuple, Any


def get_annotation_complexity(annotation_node, default_complexity: int = 1) -> int:
    if isinstance(annotation_node, ast.Str):
        try:
            annotation_node = ast.parse(annotation_node.s).body[0].value  # type: ignore
        except (SyntaxError, IndexError):
            return default_complexity
    if isinstance(annotation_node, ast.Subscript):
        return 1 + get_annotation_complexity(annotation_node.slice.value)  # type: ignore
    if isinstance(annotation_node, ast.Tuple):
        return max((get_annotation_complexity(n) for n in annotation_node.elts), default=1)
    return default_complexity


def validate_annotations_in_ast_node(node, max_annotations_complexity) -> List[Tuple[Any, int]]:
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
                complexity,
            ))
    return too_difficult_annotations

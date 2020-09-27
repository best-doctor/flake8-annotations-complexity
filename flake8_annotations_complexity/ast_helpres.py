import ast
from typing import List


def get_annotation_nodes(tree) -> List[ast.AST]:
    func_defs = [
        f for f in ast.walk(tree)
        if isinstance(f, ast.FunctionDef)
    ]
    annotations: List[ast.AST] = []
    for funcdef in func_defs:
        annotations += list(filter(None, (a.annotation for a in funcdef.args.args)))
        if funcdef.returns:
            annotations.append(funcdef.returns)
    annotations += [a.annotation for a in ast.walk(tree) if isinstance(a, ast.AnnAssign) and a.annotation]
    return annotations

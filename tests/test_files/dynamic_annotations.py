from typing import (
    List,
    Dict,
    Optional,
    Tuple,
    Literal,
)


def foo() -> List[int]:
    return [1]


def bar(arg1: str, arg2: Tuple[List[int], Optional[Dict[str, int]]]) -> int:
    return 1


def gaz() -> Literal['regular', 'raise', 'is']:
    raise Exception

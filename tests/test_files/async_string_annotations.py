from typing import Dict, List, Optional, Tuple


async def foo() -> 'List[int]':
    return [1]


async def bar(arg: 'Tuple[List[Optional[Dict[str, int]]], int]') -> 'int':
    return 1

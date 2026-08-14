from typing import Dict, List, Optional, Tuple


async def foo() -> List[int]:
    return [1]


async def bar(arg1: str, arg2: Tuple[List[int], Optional[Dict[str, int]]]) -> int:
    return 1

from collections.abc import AsyncIterator
from typing import Dict, List, Optional, Tuple


class Service:
    async def fetch(self, arg: Tuple[List[Optional[Dict[str, int]]], int]) -> None:
        pass

    async def stream(self) -> AsyncIterator[Tuple[List[Optional[Dict[str, int]]], int]]:
        yield [], 1


async def outer() -> None:
    async def inner(arg: Tuple[List[Optional[Dict[str, int]]], int]) -> None:
        pass

    local: Tuple[List[Optional[Dict[str, int]]], int] = ([], 1)

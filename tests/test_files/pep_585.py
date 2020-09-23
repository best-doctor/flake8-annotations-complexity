from __future__ import annotations

from collections import defaultdict, ChainMap, Counter, deque


# Taken from https://www.python.org/dev/peps/pep-0585/
def find(haystack: dict[str, list[int]]) -> int:
    return 0


l: list[str] = []
cm: ChainMap[str, list[str]]

# Taken from https://github.com/python/mypy/blob/master/test-data/unit/check-future.test
t1: type[int]
t2: list[int]
t3: dict[int, int]
t4: tuple[int, str, int]

c1: defaultdict[int, int]
c2: ChainMap[int, int]
c3: Counter[int]
c4: deque[int]

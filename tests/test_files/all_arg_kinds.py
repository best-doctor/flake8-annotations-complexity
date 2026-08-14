from typing import Dict, List, Optional, Tuple


def all_kinds(
    pos_only: Tuple[List[Optional[Dict[str, int]]], int],
    /,
    regular: Tuple[List[Optional[Dict[str, int]]], int],
    *args: Tuple[List[Optional[Dict[str, int]]], int],
    kw_only: Tuple[List[Optional[Dict[str, int]]], int],
    **kwargs: Tuple[List[Optional[Dict[str, int]]], int],
) -> None:
    pass

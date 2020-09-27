from typing import Any, Dict, List, Optional, Tuple

foo: Tuple[str, str, str, int, List, Any, str, Dict, int] = tuple()

bar: 'Tuple[str, str, str, int, List, Any, str, Dict, int]' = tuple()

egg: Tuple[str, str, str, int, List, Any, List[int], Optional[Dict[str, int]]] = tuple()

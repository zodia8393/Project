from dataclasses import dataclass
from typing import Any

@dataclass
class Action:
    type: str
    value: Any = None
    image: str = None
    confidence: float = 0.8
    timeout: int = 10
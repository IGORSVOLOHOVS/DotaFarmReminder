from dataclasses import dataclass, field
from typing import List

@dataclass
class Hint:
    time: str
    text: str

@dataclass
class HintState:
    current_role: str = "support"
    hints: List[Hint] = field(default_factory=list)
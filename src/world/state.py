from dataclasses import dataclass, field
from typing import List

from beast.beast import Beast


@dataclass
class State:
    active: bool = True
    beasts: List[Beast] = field(default_factory=list)

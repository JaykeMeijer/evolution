from dataclasses import dataclass, field
from typing import List

from beast.beast import Beast


@dataclass
class State:
    beasts: List[Beast] = field(default_factory=list)

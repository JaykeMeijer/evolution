from dataclasses import dataclass, field
from typing import List, Optional

from beast.beast import Beast
from datastructures.quadtree import QuadTree


@dataclass
class State:
    simulation_paused = False
    active: bool = True
    beasts: List["Beast"] = field(default_factory=list)
    tree: Optional[QuadTree] = None


state = State()

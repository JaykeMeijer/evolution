from dataclasses import dataclass, field
from typing import List, Optional

from evolution.beast.beast import Beast
from evolution.datastructures.quadtree import QuadTree


@dataclass
class State:
    simulation_paused = False
    active: bool = True
    perform_step: bool = False
    beasts: List["Beast"] = field(default_factory=list)
    tree: Optional[QuadTree] = None


state = State()

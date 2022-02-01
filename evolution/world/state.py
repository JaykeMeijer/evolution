from dataclasses import dataclass, field
from typing import List, Optional

from evolution.beast.beast import Beast
from evolution.datastructures.kdtree import KDTree


@dataclass
class State:
    simulation_paused = False
    active: bool = True
    perform_step: bool = False
    beasts: List["Beast"] = field(default_factory=list)
    tree: Optional[KDTree] = None

    render_nearest_mate: bool = False
    render_kdtree: bool = False
    render_beast_name: bool = False


state = State()

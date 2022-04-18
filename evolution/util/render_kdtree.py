# TODO: Implement for Rust KDTree
import math
import random
from typing import Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import pygame

from evolution.beast.beast import Beast
from evolution.datastructures.kdtree import KDTree

mpl.use("Agg")


def render_tree(tree: KDTree):
    G = nx.DiGraph()
    _add_to_graph(tree, G)
    pos = hierarchy_pos(G, width=2 * math.pi, xcenter=0)
    pos = {u: (r * math.cos(theta), r * math.sin(theta)) for u, (theta, r) in pos.items()}
    fig = plt.figure(0, (4, 4), dpi=200)
    fig.clear()
    nx.draw(
        G,
        pos,
        node_color=[_get_node_color(node) for node in G.nodes()],
        node_size=50,
        width=1,
    )
    nx.draw_networkx_labels(
        G,
        pos,
        labels={node: node.point.obj.id for node in G.nodes()},
        font_size=6,
    )
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels={(n1, n2): G[n1][n2]["section"] for n1, n2 in G.edges()},
        font_size=6,
    )
    fig.canvas.draw()
    surface = pygame.surface.Surface(fig.canvas.get_width_height())
    surface.blit(pygame.image.fromstring(fig.canvas.tostring_rgb(), fig.canvas.get_width_height(), "RGB"), (0, 0))
    return surface


def _add_to_graph(tree: KDTree, G: nx.DiGraph):
    G.add_node(tree)
    if tree.left is not None:
        G.add_edge(tree, tree.left, section="L")
        _add_to_graph(tree.left, G)
    if tree.right is not None:
        G.add_edge(tree, tree.right, section="R")
        _add_to_graph(tree.right, G)


def _get_node_color(node: KDTree) -> Tuple[float, float, float]:
    assert isinstance(node.point.obj, Beast)
    c = node.point.obj.color
    return (c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)


def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    """
    if not nx.is_tree(G):
        raise TypeError("cannot use hierarchy_pos on a graph that is not a tree")

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
        """
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed
        """
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(
                    G,
                    child,
                    width=dx,
                    vert_gap=vert_gap,
                    vert_loc=vert_loc - vert_gap,
                    xcenter=nextx,
                    pos=pos,
                    parent=root,
                )
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

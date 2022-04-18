try:
    from evolution.datastructures.kdtree.kdtree_rust import KDTree, KDTreePoint
except ImportError:
    from evolution.datastructures.kdtree.kdtree import KDTree, KDTreePoint  # type: ignore
    print("Warning - Not using Rust version of KDTree implementation - worse performance is to be expected")

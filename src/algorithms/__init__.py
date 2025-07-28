"""
Algorithms for finding maximum inscribed rectangles in polygons.
"""

from .convex_algorithm import find_max_rectangle_convex
from .general_algorithm import find_max_rectangle_general

__all__ = [
    'find_max_rectangle_convex',
    'find_max_rectangle_general'
] 
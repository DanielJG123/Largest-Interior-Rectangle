"""
Maximum Inscribed Rectangle Finder

A package for finding the largest possible rectangle that can be inscribed within a given polygon.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .algorithms.convex_algorithm import find_max_rectangle_convex
from .algorithms.general_algorithm import find_max_rectangle_general
from .visualization.plotter import plot_polygon_with_rectangle

__all__ = [
    'find_max_rectangle_convex',
    'find_max_rectangle_general', 
    'plot_polygon_with_rectangle'
] 
"""
Common geometric utility functions used across the algorithms.
"""

import numpy as np
import math
from typing import Tuple, List


def azimuth(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate the azimuth angle between two points.
    
    Args:
        point1: First point as (x, y) tuple
        point2: Second point as (x, y) tuple
        
    Returns:
        Azimuth angle in radians
    """
    delta_y = point2[1] - point1[1]
    delta_x = point2[0] - point1[0]
    return np.arctan2(delta_y, delta_x)


def increment(angle: float, distance: float) -> np.ndarray:
    """
    Calculate the increment vector given an angle and distance.
    
    Args:
        angle: Angle in radians
        distance: Distance to travel
        
    Returns:
        Increment vector as numpy array [dx, dy]
    """
    return np.array([np.cos(angle) * distance, np.sin(angle) * distance], dtype=float)


def sort_rectangle_coords(coords: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Sort rectangle coordinates for proper plotting order.
    
    Args:
        coords: List of 4 coordinate points defining a rectangle
        
    Returns:
        Sorted coordinates in plotting order
    """
    # Sort coordinates based on distance from the first point
    sorted_coords = sorted(coords, key=lambda k: math.dist(k, coords[0]))
    return sorted_coords[0], sorted_coords[1], sorted_coords[3], sorted_coords[2] 
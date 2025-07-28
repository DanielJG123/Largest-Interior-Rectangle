"""
Polygon processing utilities for sampling and analyzing polygon boundaries.
"""

import numpy as np
import math
from shapely.geometry import Polygon
from .geometry_utils import azimuth, increment


def split_into_points(polygon: Polygon, point_gap: float) -> np.ndarray:
    """
    Split polygon boundary into evenly spaced points.
    
    Args:
        polygon: Shapely polygon object
        point_gap: Distance between consecutive points
        
    Returns:
        Array of points along the polygon boundary
    """
    coords = list(polygon.exterior.coords[:-1])  # Remove duplicate last point
    edge_points = np.array([coords[0]], dtype=float)
    
    for i, vertex2 in enumerate(coords[1:], 1):
        vertex1 = coords[i-1]
        angle = azimuth(vertex1, vertex2)
        line_point_number = int(math.dist(vertex1, vertex2) // point_gap)
        diff = increment(angle, point_gap)
        
        for _ in range(line_point_number):
            new_point = edge_points[-1] + diff
            edge_points = np.concatenate((edge_points, [new_point]))
        
        end_point = np.array(vertex2, dtype=float)
        edge_points = np.concatenate((edge_points, [end_point]))
    
    # Handle the last edge (back to start)
    vertex2 = coords[0]
    vertex1 = coords[-1]
    angle = azimuth(vertex1, vertex2)
    line_point_number = int(math.dist(vertex1, vertex2) // point_gap)
    diff = increment(angle, point_gap)
    
    for _ in range(line_point_number):
        new_point = edge_points[-1] + diff
        edge_points = np.concatenate((edge_points, [new_point]))
    
    end_point = np.array(vertex2, dtype=float)
    edge_points = np.concatenate((edge_points, [end_point]))
    
    return edge_points


def min_extension(polygon: Polygon) -> float:
    """
    Calculate the minimum extension distance that covers the entire polygon.
    
    Args:
        polygon: Shapely polygon object
        
    Returns:
        Minimum extension distance
    """
    bounds = polygon.bounds
    return math.dist((bounds[0], bounds[1]), (bounds[2], bounds[3]))


def tiny_increment(polygon: Polygon, point_gap: float) -> float:
    """
    Calculate a small increment value for interior direction checking.
    
    Args:
        polygon: Shapely polygon object
        point_gap: Point gap used for sampling
        
    Returns:
        Tiny increment value
    """
    return point_gap / min_extension(polygon) 
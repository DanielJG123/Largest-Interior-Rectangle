"""
Algorithm for finding maximum inscribed rectangles in arbitrary polygons.
"""

import numpy as np
import math
from shapely.geometry import LineString, Polygon
from shapely import transform
from ..core.geometry_utils import azimuth, increment, sort_rectangle_coords
from ..core.polygon_processor import split_into_points, min_extension, tiny_increment


def extend_perpendicular(point1: np.ndarray, point2: np.ndarray, polygon: Polygon, 
                        tiny_increment_value: float) -> tuple:
    """
    Find the biggest rectangle possible given 2 eligible points.
    
    Args:
        point1: First point
        point2: Second point
        polygon: Shapely polygon object
        tiny_increment_value: Small increment value
        
    Returns:
        Tuple of (side_length, angle, point1, point2)
    """
    angle = azimuth(point1, point2)
    line = LineString([point1, point2])
    inc = increment(angle + np.pi/2, tiny_increment_value)
    extends = 0
    
    # Linearly transform line until it intersects an exterior side of the polygon
    while polygon.contains(line):
        line = transform(line, lambda x: x + inc)
        extends += 1
    
    side = (extends - 1) * tiny_increment_value
    return side, angle + (np.pi/2), point1, point2


def find_max_rectangle_general(polygon_coords: list, point_gap: float = 0.026) -> tuple:
    """
    Find the maximum inscribed rectangle in an arbitrary polygon.
    
    Args:
        polygon_coords: List of (x, y) coordinates defining the polygon
        point_gap: Distance between sampled points (default: 0.026)
        
    Returns:
        Tuple of (side_length, angle, point1, point2) defining the rectangle
    """
    polygon = Polygon(polygon_coords)
    tiny_increment_value = tiny_increment(polygon, point_gap)
    area = 0.00001
    edge = split_into_points(polygon, point_gap)
    extension_length = min_extension(polygon)
    
    for point1 in edge:
        for point2 in edge:
            if np.any(point1 != point2):
                if polygon.contains(LineString((point1, point2))):  # Check if points are eligible
                    distance = math.dist(point1, point2)
                    if distance > area / extension_length:
                        discovery = extend_perpendicular(point1, point2, polygon, tiny_increment_value)
                        area_found = discovery[0] * distance
                        if area_found > area:
                            area = area_found
                            final = discovery
    
    return final


def find_final_rectangle(side: float, angle: float, point1: np.ndarray, 
                        point2: np.ndarray) -> tuple:
    """
    Find the complete rectangle coordinates after finding the base points.
    
    Args:
        side: Side length of the rectangle
        angle: Angle of the rectangle
        point1: First base point
        point2: Second base point
        
    Returns:
        Tuple of four rectangle corner coordinates
    """
    coord3 = point1 + increment(angle, side)
    coord4 = point2 + increment(angle, side)
    return point1, point2, coord3, coord4 
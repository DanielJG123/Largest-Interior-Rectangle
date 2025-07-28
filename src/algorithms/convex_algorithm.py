"""
Algorithm for finding maximum inscribed rectangles in convex polygons.
"""

import numpy as np
import math
from shapely.geometry import Point, LineString, Polygon
from ..core.geometry_utils import azimuth, increment, sort_rectangle_coords
from ..core.polygon_processor import split_into_points, min_extension, tiny_increment


def extension_interior_check(point1: np.ndarray, point2: np.ndarray, angle: float, polygon: Polygon, tiny_increment_value: float, clockwise: bool = True) -> bool:
    """
    Check if the extension will be towards the inside of the shape.
    
    Args:
        point1: First point
        point2: Second point
        angle: Angle of the line
        polygon: Shapely polygon object
        tiny_increment_value: Small increment for testing
        clockwise: Direction of rotation
        
    Returns:
        True if both points extend inside
    """
    switch = 1 if clockwise else -1
    perpendicular = increment(angle + (np.pi/2) * switch, tiny_increment_value)
    extended_point1 = Point(point1[0] + perpendicular[0], point1[1] + perpendicular[1])
    extended_point2 = Point(point2[0] + perpendicular[0], point2[1] + perpendicular[1])
    return polygon.contains_properly(extended_point1) and polygon.contains_properly(extended_point2)


def extend_line(point: np.ndarray, angle: float, extension_length: float, tiny_increment_value: float) -> LineString:
    """
    Extend line by minimum distance that always covers the shape.
    
    Args:
        point: Starting point
        angle: Angle of extension
        extension_length: Length to extend
        tiny_increment_value: Small increment value
        
    Returns:
        Extended line as LineString
    """
    end_point = point + increment(angle, extension_length)
    start_point = point + increment(angle, tiny_increment_value)
    return LineString((start_point, end_point))


def extend_perpendicular(point1: np.ndarray, point2: np.ndarray, polygon: Polygon, extension_length: float, tiny_increment_value: float) -> float:
    """
    Extend line until intersection occurs.
    
    Args:
        point1: First point
        point2: Second point
        polygon: Shapely polygon object
        extension_length: Length to extend
        tiny_increment_value: Small increment value
        
    Returns:
        Side length of the rectangle
    """
    angle = azimuth(point1, point2)
    
    if extension_interior_check(point1, point2, angle, polygon, tiny_increment_value):
        crosses_left = polygon.intersection(extend_line(point1, angle + np.pi/2, extension_length, tiny_increment_value))
        crosses_right = polygon.intersection(extend_line(point2, angle + np.pi/2, extension_length, tiny_increment_value))
        
        if crosses_left.geom_type == 'MultiLineString':
            crosses_left = crosses_left.geoms[0]
        if crosses_right.geom_type == 'MultiLineString':
            crosses_right = crosses_right.geoms[0]
            
        side = min(math.dist(crosses_left.coords[1], point1), math.dist(crosses_right.coords[1], point2))
        return side
        
    elif extension_interior_check(point1, point2, angle, polygon, tiny_increment_value, False):
        crosses_left = polygon.intersection(extend_line(point1, angle - np.pi/2, extension_length, tiny_increment_value))
        crosses_right = polygon.intersection(extend_line(point2, angle - np.pi/2, extension_length, tiny_increment_value))
        
        if crosses_left.geom_type == 'MultiLineString':
            crosses_left = crosses_left.geoms[0]
        if crosses_right.geom_type == 'MultiLineString':
            crosses_right = crosses_right.geoms[0]
            
        side = min(math.dist(crosses_left.coords[1], point1), math.dist(crosses_right.coords[1], point2))
        return side
    else:
        return 0


def find_max_rectangle_convex(polygon_coords: list, point_gap: float = 0.015) -> tuple:
    """
    Find the maximum inscribed rectangle in a convex polygon.
    
    Args:
        polygon_coords: List of (x, y) coordinates defining the polygon
        point_gap: Distance between sampled points (default: 0.015)
        
    Returns:
        Tuple of (area, (point1, point2)) where point1 and point2 define the base of the rectangle
    """
    polygon = Polygon(polygon_coords)
    tiny_increment_value = tiny_increment(polygon, point_gap)
    area = 0.00001
    edge = split_into_points(polygon, point_gap)
    extension_length = min_extension(polygon)
    
    for point1 in edge:
        for point2 in edge:
            if np.any(point1 != point2):
                distance = math.dist(point1, point2)
                if distance > area / extension_length:
                    area_found = extend_perpendicular(point1, point2, polygon, extension_length, tiny_increment_value) * distance
                    if area_found > area:
                        area = area_found
                        coords = (point1, point2)
    
    return area, coords


def find_final_rectangle(point1: np.ndarray, point2: np.ndarray, polygon: Polygon, tiny_increment_value: float) -> tuple:
    """
    Find the complete rectangle coordinates after finding the base points.
    
    Args:
        point1: First base point
        point2: Second base point
        polygon: Shapely polygon object
        tiny_increment_value: Small increment value
        
    Returns:
        Tuple of four rectangle corner coordinates
    """
    angle = azimuth(point1, point2)
    extension_length = min_extension(polygon)
    
    if extension_interior_check(point1, point2, angle, polygon, tiny_increment_value):
        crosses_left = polygon.intersection(extend_line(point1, angle + np.pi/2, extension_length, tiny_increment_value))
        crosses_right = polygon.intersection(extend_line(point2, angle + np.pi/2, extension_length, tiny_increment_value))
        
        if math.dist(crosses_left.coords[1], point1) < math.dist(crosses_right.coords[1], point2):
            coord3 = np.array(crosses_left.coords[1])
            coord4 = point2 + increment(azimuth(point1, coord3), math.dist(coord3, point1))
        else:
            coord3 = np.array(crosses_right.coords[1])
            coord4 = point1 + increment(azimuth(point2, coord3), math.dist(coord3, point2))
            
    elif extension_interior_check(point1, point2, angle, polygon, tiny_increment_value, False):
        crosses_left = polygon.intersection(extend_line(point1, angle - np.pi/2, extension_length, tiny_increment_value))
        crosses_right = polygon.intersection(extend_line(point2, angle - np.pi/2, extension_length, tiny_increment_value))
        
        if math.dist(crosses_left.coords[1], point1) < math.dist(crosses_right.coords[1], point2):
            coord3 = np.array(crosses_left.coords[1])
            coord4 = point2 + increment(azimuth(point1, coord3), math.dist(coord3, point1))
        else:
            coord3 = np.array(crosses_right.coords[1])
            coord4 = point1 + increment(azimuth(point2, coord3), math.dist(coord3, point2))
    else:
        raise ValueError("Could not determine rectangle orientation")
        
    return point1, point2, coord3, coord4 
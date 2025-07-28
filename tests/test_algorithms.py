"""
Tests for the maximum inscribed rectangle algorithms.
"""

import pytest
import numpy as np
from shapely.geometry import Polygon
from src.algorithms.convex_algorithm import find_max_rectangle_convex
from src.algorithms.general_algorithm import find_max_rectangle_general


def test_convex_algorithm_square():
    """Test convex algorithm on a square."""
    # Simple square polygon
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    
    area, (point1, point2) = find_max_rectangle_convex(square, point_gap=0.1)
    
    # The maximum inscribed rectangle in a square should be the square itself
    assert area > 0.9  # Should be close to 1.0
    assert isinstance(point1, np.ndarray)
    assert isinstance(point2, np.ndarray)


def test_convex_algorithm_rectangle():
    """Test convex algorithm on a rectangle."""
    # Rectangle polygon
    rectangle = [(0, 0), (2, 0), (2, 1), (0, 1)]
    
    area, (point1, point2) = find_max_rectangle_convex(rectangle, point_gap=0.1)
    
    # Should find a rectangle with area close to 2.0
    assert area > 1.8
    assert isinstance(point1, np.ndarray)
    assert isinstance(point2, np.ndarray)


def test_general_algorithm_square():
    """Test general algorithm on a square."""
    # Simple square polygon
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    
    result = find_max_rectangle_general(square, point_gap=0.1)
    side, angle, point1, point2 = result
    
    # Should find a reasonable rectangle
    assert side > 0
    assert isinstance(point1, np.ndarray)
    assert isinstance(point2, np.ndarray)


def test_general_algorithm_complex():
    """Test general algorithm on a more complex polygon."""
    # L-shaped polygon
    l_shape = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
    
    result = find_max_rectangle_general(l_shape, point_gap=0.1)
    side, angle, point1, point2 = result
    
    # Should find a reasonable rectangle
    assert side > 0
    assert isinstance(point1, np.ndarray)
    assert isinstance(point2, np.ndarray)


def test_polygon_validation():
    """Test that algorithms handle invalid polygons gracefully."""
    # Invalid polygon (not enough points)
    invalid_polygon = [(0, 0), (1, 0)]
    
    with pytest.raises(Exception):
        find_max_rectangle_convex(invalid_polygon)
    
    with pytest.raises(Exception):
        find_max_rectangle_general(invalid_polygon) 
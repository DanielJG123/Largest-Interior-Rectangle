"""
Tests for geometry utility functions.
"""

import pytest
import numpy as np
from src.core.geometry_utils import azimuth, increment, sort_rectangle_coords


def test_azimuth():
    """Test azimuth calculation."""
    # Test horizontal line
    assert abs(azimuth((0, 0), (1, 0)) - 0) < 1e-10
    
    # Test vertical line
    assert abs(azimuth((0, 0), (0, 1)) - np.pi/2) < 1e-10
    
    # Test diagonal line
    assert abs(azimuth((0, 0), (1, 1)) - np.pi/4) < 1e-10


def test_increment():
    """Test increment vector calculation."""
    # Test horizontal increment
    inc = increment(0, 2)
    assert np.allclose(inc, [2, 0])
    
    # Test vertical increment
    inc = increment(np.pi/2, 3)
    assert np.allclose(inc, [0, 3])
    
    # Test diagonal increment
    inc = increment(np.pi/4, np.sqrt(2))
    assert np.allclose(inc, [1, 1])


def test_sort_rectangle_coords():
    """Test rectangle coordinate sorting."""
    coords = [
        np.array([1, 1]),
        np.array([0, 0]),
        np.array([1, 0]),
        np.array([0, 1])
    ]
    
    sorted_coords = sort_rectangle_coords(coords)
    assert len(sorted_coords) == 4
    
    # Check that all original coordinates are present
    for coord in coords:
        assert any(np.allclose(coord, sorted_coord) for sorted_coord in sorted_coords) 
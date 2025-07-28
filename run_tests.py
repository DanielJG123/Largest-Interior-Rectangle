#!/usr/bin/env python3
"""
Simple test runner for the maximum inscribed rectangle package.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_basic_tests():
    """Run basic functionality tests."""
    print("Running basic tests...")
    
    try:
        # Test imports
        from src.core.geometry_utils import azimuth, increment
        from src.algorithms.convex_algorithm import find_max_rectangle_convex
        from src.algorithms.general_algorithm import find_max_rectangle_general
        print("✓ All imports successful")
        
        # Test basic geometry functions
        angle = azimuth((0, 0), (1, 1))
        assert abs(angle - 0.7853981633974483) < 1e-10
        print("✓ Geometry utilities working")
        
        # Test convex algorithm on simple square
        square = [(0, 0), (1, 0), (1, 1), (0, 1)]
        area, coords = find_max_rectangle_convex(square, point_gap=0.1)
        assert area > 0
        print("✓ Convex algorithm working")
        
        # Test general algorithm on simple square
        result = find_max_rectangle_general(square, point_gap=0.1)
        side, angle, p1, p2 = result
        assert side > 0
        print("✓ General algorithm working")
        
        print("\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1) 
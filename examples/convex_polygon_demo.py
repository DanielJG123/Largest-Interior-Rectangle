"""
Demonstration of the convex polygon maximum inscribed rectangle algorithm.
This is based on the original Rectengles_convex_shapes.py file.
"""

import time
import random
import numpy as np
from polygenerator import random_convex_polygon
from shapely.geometry import Polygon

from src.algorithms.convex_algorithm import (
    find_max_rectangle_convex, 
    find_final_rectangle
)
from src.core.polygon_processor import tiny_increment
from src.visualization.plotter import plot_polygon_with_rectangle


def demo_convex_polygon():
    """Demonstrate the convex polygon algorithm."""
    # Set random seed for reproducibility
    random.seed(10)
    
    # Generate a random convex polygon
    polygon_coords = random_convex_polygon(num_points=20)
    print(f"Generated convex polygon with {len(polygon_coords)} vertices")
    
    # Find maximum inscribed rectangle
    start_time = time.time()
    point_gap = 0.015
    result = find_max_rectangle_convex(polygon_coords, point_gap)
    
    area, (point1, point2) = result
    print(f"Maximum rectangle area: {area:.6f}")
    print(f"Base points: {point1}, {point2}")
    
    # Find complete rectangle coordinates
    polygon = Polygon(polygon_coords)
    tiny_inc = tiny_increment(polygon, point_gap)
    rectangle_coords = find_final_rectangle(point1, point2, polygon, tiny_inc)
    
    end_time = time.time()
    print(f"Computation time: {end_time - start_time:.4f} seconds")
    
    # Plot the result
    plot_polygon_with_rectangle(
        polygon_coords, 
        list(rectangle_coords), 
        output_file="convex_polygon_result.png"
    )
    
    return polygon_coords, rectangle_coords, area


def demo_multiple_convex_polygons():
    """Demonstrate the algorithm on multiple convex polygons."""
    results = []
    
    for i in range(3):
        print(f"\n--- Convex Polygon {i+1} ---")
        random.seed(10 + i)
        
        polygon_coords = random_convex_polygon(num_points=15 + i*5)
        result = find_max_rectangle_convex(polygon_coords, point_gap=0.02)
        
        area, (point1, point2) = result
        polygon = Polygon(polygon_coords)
        tiny_inc = tiny_increment(polygon, 0.02)
        rectangle_coords = find_final_rectangle(point1, point2, polygon, tiny_inc)
        
        results.append({
            'polygon': polygon_coords,
            'rectangle': list(rectangle_coords),
            'area': area
        })
        
        print(f"Area: {area:.6f}")
        
        # Plot each result
        plot_polygon_with_rectangle(
            polygon_coords, 
            list(rectangle_coords), 
            output_file=f"convex_polygon_{i+1}.png",
            show_plot=False
        )
    
    return results


if __name__ == "__main__":
    print("=== Convex Polygon Maximum Inscribed Rectangle Demo ===\n")
    
    # Single polygon demo
    demo_convex_polygon()
    
    # Multiple polygons demo
    print("\n" + "="*50)
    demo_multiple_convex_polygons() 
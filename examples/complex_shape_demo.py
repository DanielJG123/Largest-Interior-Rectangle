"""
Demonstration of the general polygon maximum inscribed rectangle algorithm.
This is based on the original Rectangle_crazy_shapes.py file.
"""

import time
import random
import numpy as np
from polygenerator import random_polygon
from shapely.geometry import Polygon

from src.algorithms.general_algorithm import (
    find_max_rectangle_general, 
    find_final_rectangle
)
from src.visualization.plotter import plot_polygon_with_rectangle


def demo_complex_polygon():
    """Demonstrate the general polygon algorithm on a complex shape."""
    # Set random seed for reproducibility
    random.seed(5)
    
    # Generate a random complex polygon
    polygon_coords = random_polygon(num_points=21)
    print(f"Generated complex polygon with {len(polygon_coords)} vertices")
    
    # Find maximum inscribed rectangle
    start_time = time.time()
    point_gap = 0.026  # Distance of points along outline of shape
    result = find_max_rectangle_general(polygon_coords, point_gap)
    
    side, angle, point1, point2 = result
    rectangle_coords = find_final_rectangle(side, angle, point1, point2)
    area = side * np.linalg.norm(point2 - point1)
    
    end_time = time.time()
    print(f"Maximum rectangle area: {area:.6f}")
    print(f"Rectangle dimensions: {side:.6f} x {np.linalg.norm(point2 - point1):.6f}")
    print(f"Computation time: {end_time - start_time:.4f} seconds")
    
    # Plot the result
    plot_polygon_with_rectangle(
        polygon_coords, 
        list(rectangle_coords), 
        output_file="complex_polygon_result.png"
    )
    
    return polygon_coords, rectangle_coords, area


def demo_multiple_complex_polygons():
    """Demonstrate the algorithm on multiple complex polygons."""
    results = []
    
    for i in range(3):
        print(f"\n--- Complex Polygon {i+1} ---")
        random.seed(5 + i)
        
        polygon_coords = random_polygon(num_points=18 + i*3)
        result = find_max_rectangle_general(polygon_coords, point_gap=0.03)
        
        side, angle, point1, point2 = result
        rectangle_coords = find_final_rectangle(side, angle, point1, point2)
        area = side * np.linalg.norm(point2 - point1)
        
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
            output_file=f"complex_polygon_{i+1}.png",
            show_plot=False
        )
    
    return results


def demo_parameter_comparison():
    """Compare different point_gap values and their effects."""
    random.seed(42)
    polygon_coords = random_polygon(num_points=25)
    
    point_gaps = [0.05, 0.03, 0.02, 0.015]
    results = []
    
    print("=== Parameter Comparison ===")
    print("Comparing different point_gap values:")
    
    for point_gap in point_gaps:
        start_time = time.time()
        result = find_max_rectangle_general(polygon_coords, point_gap)
        end_time = time.time()
        
        side, angle, point1, point2 = result
        rectangle_coords = find_final_rectangle(side, angle, point1, point2)
        area = side * np.linalg.norm(point2 - point1)
        
        results.append({
            'point_gap': point_gap,
            'area': area,
            'time': end_time - start_time,
            'rectangle': list(rectangle_coords)
        })
        
        print(f"point_gap={point_gap}: area={area:.6f}, time={end_time - start_time:.4f}s")
    
    # Plot the best result
    best_result = max(results, key=lambda x: x['area'])
    plot_polygon_with_rectangle(
        polygon_coords, 
        best_result['rectangle'], 
        output_file="parameter_comparison_best.png"
    )
    
    return results


if __name__ == "__main__":
    print("=== Complex Polygon Maximum Inscribed Rectangle Demo ===\n")
    
    # Single complex polygon demo
    demo_complex_polygon()
    
    # Multiple complex polygons demo
    print("\n" + "="*50)
    demo_multiple_complex_polygons()
    
    # Parameter comparison demo
    print("\n" + "="*50)
    demo_parameter_comparison() 
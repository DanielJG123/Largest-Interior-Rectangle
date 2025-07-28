"""
Visualization utilities for polygons and rectangles.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
from ..core.geometry_utils import sort_rectangle_coords


def plot_polygon_with_rectangle(polygon_coords: List[Tuple[float, float]], 
                               rectangle_coords: List[np.ndarray], 
                               output_file: str = None, 
                               show_plot: bool = True) -> None:
    """
    Plot a polygon with its maximum inscribed rectangle.
    
    Args:
        polygon_coords: List of (x, y) coordinates defining the polygon
        rectangle_coords: List of 4 rectangle corner coordinates
        output_file: Optional file path to save the plot
        show_plot: Whether to display the plot
    """
    plt.figure(figsize=(10, 8))
    plt.gca().set_aspect("equal")
    
    # Plot polygon vertices with labels
    for i, (x, y) in enumerate(polygon_coords):
        plt.text(x, y, str(i), horizontalalignment="center", verticalalignment="center", 
                fontsize=8, color='red')
    
    # Plot polygon boundary
    polygon_plot = polygon_coords + [polygon_coords[0]]  # Close the polygon
    xs, ys = zip(*polygon_plot)
    plt.plot(xs, ys, "r-", linewidth=2, label="Polygon")
    
    # Plot rectangle
    sorted_rect = sort_rectangle_coords(rectangle_coords)
    rect_plot = list(sorted_rect) + [sorted_rect[0]]  # Close the rectangle
    rect_xs, rect_ys = zip(*rect_plot)
    plt.plot(rect_xs, rect_ys, "b-", linewidth=2, label="Maximum Rectangle")
    
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Polygon with Maximum Inscribed Rectangle")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    
    if show_plot:
        plt.show()
    else:
        plt.close()


def plot_random_polygon(polygon_coords: List[Tuple[float, float]], 
                       rectangle_coords: List[np.ndarray], 
                       output_file: str) -> None:
    """
    Plot a random polygon with its maximum inscribed rectangle (legacy function).
    
    Args:
        polygon_coords: List of (x, y) coordinates defining the polygon
        rectangle_coords: List of 4 rectangle corner coordinates
        output_file: File path to save the plot
    """
    plt.figure()
    plt.gca().set_aspect("equal")
    
    # Plot polygon vertices with labels
    for i, (x, y) in enumerate(polygon_coords):
        plt.text(x, y, str(i), horizontalalignment="center", verticalalignment="center")
    
    # Plot polygon boundary
    polygon_plot = polygon_coords + [polygon_coords[0]]  # Close the polygon
    xs, ys = zip(*polygon_plot)
    plt.plot(xs, ys, "r-", linewidth=0.4)
    
    # Plot rectangle
    sorted_rect = sort_rectangle_coords(rectangle_coords)
    rect_plot = list(sorted_rect) + [sorted_rect[0]]  # Close the rectangle
    rect_xs, rect_ys = zip(*rect_plot)
    plt.plot(rect_xs, rect_ys, "b-", linewidth=0.2)
    
    plt.savefig(output_file, dpi=300)
    plt.show() 
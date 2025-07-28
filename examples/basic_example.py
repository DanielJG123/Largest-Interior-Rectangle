"""
Basic example demonstrating point generation in polygons.
This is based on the original example.py file.
"""

import numpy as np
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.ops import triangulate
from polygenerator import random_polygon
import random
from geopandas import GeoSeries
import matplotlib.pyplot as plt


def random_point_in_triangle(triangle):
    """Generate a random point within a triangle."""
    r1, r2 = np.random.rand(2)
    sqrt_r1 = np.sqrt(r1)
    return (1 - sqrt_r1) * triangle[0] + (sqrt_r1 * (1 - r2)) * triangle[1] + (sqrt_r1 * r2) * triangle[2]


def generate_points_in_polygon(polygon, n_points):
    """Generate n_points randomly distributed within a polygon."""
    triangles = triangulate(polygon)
    total_area = sum(tri.area for tri in triangles)
    
    points = []
    for tri in triangles:
        tri_area = tri.area
        n_tri_points = int(np.round((tri_area / total_area) * n_points))
        
        tri_coords = np.array(tri.exterior.coords[:-1])
        for _ in range(n_tri_points):
            point = random_point_in_triangle(tri_coords)
            points.append(Point(point))
    
    return MultiPoint(points)


def main():
    """Run the basic example."""
    # Example polygon (a random quadrilateral)
    polygon = Polygon([(0, 0), (2, 0), (1.5, 1), (0, 2)])
    
    # Plot the polygon
    GeoSeries(polygon).plot()
    plt.title("Example Polygon")
    plt.show()
    
    # Generate 100 points in the polygon
    n_points = 100
    points = generate_points_in_polygon(polygon, n_points)
    
    # Plot polygon with points
    ax = plt.gca()
    GeoSeries(points).plot(ax=ax)
    GeoSeries(polygon.exterior).plot(ax=ax, color='black')
    plt.title(f"Polygon with {n_points} Random Points")
    plt.show()
    
    # Convert the points to a list of coordinates
    point_coords = [p for p in points.geoms]
    print(f"Generated {len(point_coords)} points in the polygon")


if __name__ == "__main__":
    main() 
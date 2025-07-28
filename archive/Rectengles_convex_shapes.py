#%%
import time
from polygenerator import (
    random_polygon,
    random_star_shaped_polygon,
    random_convex_polygon,
)
import matplotlib.pyplot as plt
import random
import numpy as np 
import math
from shapely.geometry import Point, LineString, Polygon

def azimuth(Point1, Point2) -> float:
    '''Calculates the angle'''
    deltaY = Point2[1] - Point1[1]
    deltaX = Point2[0] - Point1[0]
    return (np.arctan2(deltaY, deltaX))

def increment(angle, dist):
    inc =np.array(([np.cos(angle)*dist, np.sin(angle)*dist]), dtype=float)
    return inc

#split up edge of polygon into many points equidistant along the perimeter
def split_into_points(linearRing, point_gap):
    edge_points = np.array([linearRing[0]], dtype=float)
    for vertex2 in linearRing[1:]:
        vertex1_index = linearRing.index(vertex2)-1
        vertex1 = linearRing[vertex1_index]
        angle = azimuth(vertex1, vertex2)
        line_point_number = int(math.dist(vertex1, vertex2)//point_gap) #number of points to find on particular line segment
        diff = increment(angle, point_gap)
        for num in range(line_point_number):
            new_point = edge_points[-1] + diff
            edge_points = np.concatenate((edge_points, [new_point]))
        end_point = np.array(vertex2, dtype=float)
        edge_points = np.concatenate((edge_points, [end_point]))
    #final vertex back to start:
    vertex2 = linearRing[0]
    vertex1 = linearRing[-1]
    angle = azimuth(vertex1, vertex2)
    line_point_number = int(math.dist(vertex1, vertex2)//point_gap)
    diff = increment(angle, point_gap)
    end_point = np.array(vertex2, dtype=float)
    for num in range(line_point_number):
        new_point = edge_points[-1] + diff
        edge_points = np.concatenate((edge_points, [new_point]))
    edge_points = np.concatenate((edge_points, [end_point]))
    return edge_points

#Checking if the extension will be towards the inside or outside of the shape
#Returns true if both points extend inside
#Checks 90 degrees in both directions
def extension_interior_check(point1, point2, angle, linearRing, tiny_increment_value, clockwise = True):
    switch = 1
    if not clockwise:
        switch = -1
    perpendicular = increment(angle + (np.pi/2)*switch, tiny_increment_value)
    extended_point1 = Point(point1[0] +perpendicular[0], point1[1] + perpendicular[1])
    extended_point2 = Point(point2[0] +perpendicular[0], point2[1] + perpendicular[1])
    return linearRing.contains_properly(extended_point1) and linearRing.contains_properly(extended_point2)

#This is the tiny line distance used to check which direction the 
#interior of the shape is from the two points that are being tested
def tiny_increment(linearRing, point_gap):
    return point_gap/min_extension(linearRing)

#Extend line by minumum distance that always covers the shape
def extend_line(point, angle, extension_length, tiny_increment_value):
    end_point = point + increment(angle, extension_length)
    start_point = point + increment(angle, tiny_increment_value)
    return LineString((start_point, end_point))

#Finding minimum distance that always covers the shape
def min_extension(linearRing):
    box = (linearRing.bounds)
    return math.dist((box[0], box[1]), (box[2], box[3]))

#Extend line until intersection occurs
def extend_perpendicular(point1, point2, linearRing, extension_length, tiny_increment_value):
    angle = azimuth(point1, point2)
    if extension_interior_check(point1, point2, angle, linearRing, tiny_increment_value):
        crosses_left = linearRing.intersection(extend_line(point1, angle + np.pi/2, extension_length, tiny_increment_value))
        crosses_right = linearRing.intersection(extend_line(point2, angle + np.pi/2, extension_length, tiny_increment_value))
        if crosses_left.geom_type == 'MultiLineString':
            crosses_left = crosses_left.geoms[0]
        if crosses_right.geom_type == 'MultiLineString':
            crosses_right = crosses_right.geoms[0]
        side = min(math.dist(crosses_left.coords[1], point1), math.dist(crosses_right.coords[1], point2))
        return side
    elif extension_interior_check(point1, point2, angle, linearRing, tiny_increment_value, False):
        crosses_left = linearRing.intersection(extend_line(point1, angle - np.pi/2, extension_length, tiny_increment_value))
        crosses_right = linearRing.intersection(extend_line(point2, angle - np.pi/2, extension_length, tiny_increment_value))
        if crosses_left.geom_type == 'MultiLineString':
            crosses_left = crosses_left.geoms[0]
        if crosses_right.geom_type == 'MultiLineString':
            crosses_right = crosses_right.geoms[0]
        side = min(math.dist(crosses_left.coords[1], point1), math.dist(crosses_right.coords[1], point2))
        return side
    else:
        return 0

#iterate through every pair of points
def test(linearRing, point_gap):
    tiny_increment_value = tiny_increment(linearRing, point_gap)
    area = 0.00001
    edge = split_into_points(polygon, point_gap)
    extension_length = min_extension(linearRing)
    for point1 in edge:
        for point2 in edge:
            if all(point1!=point2):
                distance = math.dist(point1, point2)
                if distance > area/extension_length:
                    area_found = extend_perpendicular(point1, point2, linearRing, extension_length, tiny_increment_value)*distance
                    if area_found> area:
                        area = area_found
                        coords = (point1, point2)

    return area, coords

#After finding 2 points that give the maximal rectangle
def find_final_rectangle(point1, point2, linearRing, tiny_increment_value):
    angle = azimuth(point1, point2)
    extension_length = min_extension(linearRing)
    if extension_interior_check(point1, point2, angle, linearRing, tiny_increment_value):
        crosses_left = linearRing.intersection(extend_line(point1, angle + np.pi/2, extension_length, tiny_increment_value))
        crosses_right = linearRing.intersection(extend_line(point2, angle + np.pi/2, extension_length, tiny_increment_value))
        if math.dist(crosses_left.coords[1], point1) < math.dist(crosses_right.coords[1], point2):
            coord3 = np.array(crosses_left.coords[1])
            coord4 = point2 + increment(azimuth(point1, coord3), math.dist(coord3, point1))
        else: 
            coord3 = np.array(crosses_right.coords[1])
            coord4 = point1 + increment(azimuth(point2, coord3), math.dist(coord3, point2))
    elif extension_interior_check(point1, point2, angle, linearRing, tiny_increment_value, False):
        crosses_left = linearRing.intersection(extend_line(point1, angle - np.pi/2, extension_length, tiny_increment_value))
        crosses_right = linearRing.intersection(extend_line(point2, angle - np.pi/2, extension_length, tiny_increment_value))
        if math.dist(crosses_left.coords[1], point1) < math.dist(crosses_right.coords[1], point2):
            coord3 = np.array(crosses_left.coords[1])
            coord4 = point2 + increment(azimuth(point1, coord3), math.dist(coord3, point1))
        else: 
            coord3 = np.array(crosses_right.coords[1])
            coord4 = point1 + increment(azimuth(point2, coord3), math.dist(coord3, point2))
    return point1, point2, coord3, coord4

def sort_rectangle_coords(coords):
    a = coords[0]
    sorted(coords, key=lambda k: math.dist(k, a))
    print(coords)
    return coords[0], coords[1], coords[3], coords[2]

#ploting shape
def plot_random_polygon(polygon, coords, out_file_name):
    plt.figure()
    plt.gca().set_aspect("equal")
    for i, (x, y) in enumerate(polygon):
        plt.text(x, y, str(i), horizontalalignment="center", verticalalignment="center")
    # just so that it is plotted as closed polygon
    polygon.append(polygon[0])
    xs, ys = zip(*polygon)
    plt.plot(xs, ys, "r-", linewidth=0.4)
    xs, ys = zip(*coords, coords[0])
    plt.plot(xs, ys, "b-", linewidth=0.2)
    plt.savefig(out_file_name, dpi=300)
    plt.show()

random.seed(10)
polygon = random_convex_polygon(num_points=20)
start = time.time()
point_gap = 0.015
x = test(Polygon(polygon), point_gap)
print(x)
coords = find_final_rectangle(x[1][0], x[1][1], Polygon(polygon), tiny_increment(Polygon(polygon), point_gap))
print(coords)
coords1 = sort_rectangle_coords(coords)
print(coords1)
end = time.time()
print(end - start)
plot_random_polygon(polygon, coords1, 'graph of polygon and largest rectangle')
# %%

#%%
from polygenerator import (
    random_polygon,
    random_star_shaped_polygon,
    random_convex_polygon,
)
import matplotlib.pyplot as plt
import random
import numpy as np 
import math
from shapely.geometry import LineString, Polygon
from shapely import transform

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

#This finds the biggest rectangle possible given 2 eligible points
def extend_perpendicular(point1, point2, linearRing, tiny_increment_value):
    angle = azimuth(point1, point2)
    line = LineString([point1, point2])
    inc = increment(angle+np.pi/2, tiny_increment_value)
    extends = 0
    #Linearly transforming line until it intersects an exterior side of the polygon
    while linearRing.contains(line):
        line = transform(line, lambda x: x + [inc])
        extends +=1
    side = (extends-1)*tiny_increment_value
    return side, angle+(np.pi/2), point1, point2
    
#iterate through every pair of points to find the largest eligible rectangle
def test(linearRing, point_gap):
    tiny_increment_value = tiny_increment(linearRing, point_gap)
    area = 0.00001
    edge = split_into_points(polygon, point_gap)
    extension_length = min_extension(linearRing)
    for point1 in edge:
        for point2 in edge:
            if all(point1!=point2):
                if linearRing.contains(LineString((point1, point2))): #Checking points are eligible
                    distance = math.dist(point1, point2)
                    if distance > area/extension_length:
                        discovery = extend_perpendicular(point1, point2, linearRing, tiny_increment_value)
                        area_found = discovery[0]*distance
                        if area_found> area:
                            area = area_found
                            final = discovery
    return final

#After finding 2 points that give the maximal rectangle
def find_final_rectangle(side, angle, point1, point2):
    coord3 = point1 + increment(angle, side)
    coord4 = point2 + increment(angle, side)
    return point1, point2, coord3, coord4

#sorting rectangle coordinates into plotting order
def sort_rectangle_coords(coords):
    a = coords[0]
    sorted(coords, key=lambda k: math.dist(k, a))
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
    plt.plot(xs, ys, "r-", linewidth=0.5)
    xs, ys = zip(*coords, coords[0])
    plt.plot(xs, ys, "b-", linewidth=0.3)
    plt.savefig(out_file_name, dpi=300)
    plt.show()

random.seed(5)
polygon = random_polygon(num_points=21)
#print(Polygon(polygon).length)

point_gap = 0.026 #distance of points along outline of shape used to find the rectangle
#As this value decreases, we get closer to the true maximum rectangle, but the runtime will increase

x = test(Polygon(polygon), point_gap)
coords = find_final_rectangle(x[0], x[1], x[2], x[3])
coords1 = sort_rectangle_coords(coords)
print(coords1)
plot_random_polygon(polygon, coords1, 'graph of polygon and largest rectangle')

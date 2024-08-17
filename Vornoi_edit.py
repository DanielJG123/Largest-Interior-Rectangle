
import numpy as np
from shapely import MultiPoint, Polygon, Point, normalize, voronoi_polygons, centroid, intersection, area
from shapely.ops import nearest_points
import matplotlib.pyplot as plt
from geopandas import GeoSeries
from random import uniform, seed
from polygenerator import random_polygon, random_convex_polygon
import colorsys 
  
def generate_random(number, polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(uniform(minx, maxx), uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def plot_voronai(Voron, polygon, cmap):
    ax=plt.gca()
    for i,j in enumerate(Voron.geoms):
        GeoSeries(intersection(polygon,j)).plot(ax=ax, color=[cmap[i]])
    plt.show()

def relax(points: list[Point], polygon: Polygon, iters: int, cmap, show) -> None:
    Voronoi = normalize(voronoi_polygons(MultiPoint(points)))
    centroids_ =[]
    areas= []
    if show:
        plot_voronai(Voronoi,polygon, cmap)
    for i in range(iters):
        centroids = []
        for region in Voronoi.geoms:
            p = intersection(polygon,region)
            if p.geom_type == "MultiPolygon":
                print("MultiPolygon")
                print(p)
                p = max(p.geoms, key=lambda a: area(a))
            centroids.append(centroid(p))
        centroids_.append(centroids)
        Voronoi = normalize(voronoi_polygons(MultiPoint(centroids)))
        areas.append([area(intersection(polygon,a)) for a in Voronoi.geoms])
        if show:
            plot_voronai(Voronoi, polygon, cmap)
    return centroids_[areas.index(min(areas, key=lambda k: np.var(k)))]
 
def HSVToRGB(h, s, v): 
 (r, g, b) = colorsys.hsv_to_rgb(h, s, v) 
 return (int(255*r)/255, int(255*g)/255, int(255*b)/255) 
 
def getDistinctColors(n): 
 huePartition = 1.0 / (n + 1) 
 return [HSVToRGB(huePartition * value, 1.0, 1.0) for value in range(0, n)]

def run(num: int, sides: int, show=True, convex=False):
    colors = getDistinctColors(num)
    if convex: polygon = Polygon(random_convex_polygon(sides))
    else: polygon = Polygon(random_polygon(sides))
    if show:
        GeoSeries(polygon).plot()
        plt.show()
    points = generate_random(num, polygon)
    return relax(points, polygon, 15, colors, show), polygon
seed(2)
points, polygon = run(2, 6, convex=True, show=False)
ax=plt.gca()
GeoSeries(points).plot(ax=ax)
GeoSeries(polygon.boundary).plot(ax=ax)
plt.show()
#for p in points:



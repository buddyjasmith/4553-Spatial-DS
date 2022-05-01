
#******************************************************************************
# Name:        Buddy Smith
# Assignment:  P03
# Date:        March 13, 2022
# Description: Given a list of major US cities and UFO sightings, split the
#              US map into a sectioned off voronoi map and assign each ufo
#              sighting to a section on the map.  Then create a list
#              assigning each ufo to the given section
# Sources:     I had help from Dakota, I was completely lost on the last
#              half of the assignment
import json

import geopandas
import geopandas as gpd
import numpy
import pandas as pd

import matplotlib.pyplot as plt

import shapely
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import  plot_voronoi_polys_with_points_in_area
from shapely.ops import unary_union
from rich import print as rp
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
class IWantToBelieve2:
    '''
    Class:       IWantToBelieve2
    Data Members: cities: list -> list of major us cities,
                  ufo: list -> list of ufo sightings in the us
                  us_border_shape: shape of the us border points
                  ufo_data_frame: geopanda data frame
                  boundary:
                  us_border_projection: projection of cities in us
    '''
    def __init__(self):
        self.cities = None
        self.ufo = None
        self.us_border_shape = None
        self.ufo_data_frame = None
        self.boundary = None
        self.us_border_projection = None

    def load_data(self):
        # Read in data related to assignment
        # does not need to be converted to correct point geometry, already
        #correct
        self.cities = gpd.read_file('data/cities.geojson')
        #read in csv, convert to dataframe later
        self.ufo = pd.read_csv('data/BetterUFO.csv')
        self.boundary = gpd.read_file('data/us_border_shp/us_border.shp')
        print(self.boundary.head())
        self.borders = gpd.read_file("data/us_borders.geojson")
        #create plot
        fig, ax = plt.subplots(figsize=(12, 10))
        self.borders.plot(ax=ax)
        self.ufo = geopandas.GeoDataFrame(
            self.ufo,
            geometry=geopandas.points_from_xy(
                        self.ufo.lon,
                        self.ufo.lat))
        # get shape of us, transforms crs to different reference system
        #make sure correct projection type
        self.border_proj = self.cities.to_crs(self.boundary.crs)
        #convert the points to coordinates,
        # Returns a geometry containing the union of all geometries in the GeoSeries.
        self.boundary_shape = unary_union(self.boundary.geometry)
        # create points from border projection
        coordinates = points_to_coords(self.border_proj.geometry)

        # Create voronoi diagram
        region_polys, region_pts = voronoi_regions_from_coords(
            coordinates,
            self.boundary_shape)
        #create vornoi plots
        # plot voronoi with ax, boundaryshape, regional_polys, coordinates
        # and regional points
        plot_voronoi_polys_with_points_in_area(ax,
                                               self.boundary_shape,
                                               region_polys,
                                               coordinates,
                                               region_pts)
        #no point in plotting, covered by sighting
        self.cities.plot(ax=ax, color='black', markersize=20)


        self.ufo.plot(ax=ax, color='green', markersize=.3)

        #show lat lon grid
        ax.axis('on')
        # equal sides
        plt.axis('equal')
        # set min, max values for each cartesian coordinate
        minx, miny, maxx, maxy = self.boundary.total_bounds
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)

        # Show plot of us cities and UFOS
        plt.show()

        #len = 49
        reg_poly_len = len(region_polys)
        #begin adding points at 49
        point_begin = reg_poly_len
        ufo_point_dict = dict()
        for point in list(self.ufo.values):
            # Point[7] is a Point obj
            region_polys.update({point_begin : point[7]})
            ufo_point_dict[point_begin] = point[7]
            point_begin += 1
        # create geoseries to query
        geo_series = geopandas.GeoSeries(region_polys)
        index = 0
        #set the reference system
        #self.ufo.set_crs(epsg=4326, inplace=True)

        output = []
        polypoints = []
        type_of = 'Oops'
        for i in range(0, reg_poly_len):
            # determine if single polygon or multipolygon
            if (type(geo_series[i]) == Polygon):
                type_of = 'Single'
                polypoints = numpy.asarray(geo_series[i].exterior.coords)
                polypoints = polypoints.tolist()

            elif type(geo_series[i]) == MultiPolygon:
                type_of = 'Multi'
                polypoints = []
                for polygon in geo_series[i]:

                    coords = numpy.asarray(polygon.exterior.coords)
                    coords = coords.tolist()

                    polypoints.append(coords)

            #creates rtree spatial index and queries rtree[i] 0 -49
            # containing ufo points
            query = geo_series.sindex.query(geo_series[i],
                                            predicate='contains')
            points =[]
            for point in query:
                # iterate through ufo points
                if type(geo_series[point]) == shapely.geometry.point.Point:
                    points.append([geo_series[point].x, geo_series[point].y])

            output.append({
                'type': type_of,
                'poly': polypoints,
                'points': points
            })
        # writes type of poly, polygon point, and ufo points within it
        with open('PolyPoints.json', 'w') as file:
            file.write(json.dumps(output))

        # print(type(rtree))
iwt = IWantToBelieve2()
iwt.load_data()


import json
import rtree
import geopandas
import geopandas as gpd
import numpy
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt
import geovoronoi
import descartes
import shapely
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from shapely.ops import unary_union
from rich import print as rp
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
class IWantToBelieve2:
    def __init__(self):
        self.cities = None
        self.ufo = None
        self.us_border_shape = None
        self.ufo_data_frame = None
        self.boundary = None
        self.us_border_projection = None

    def load_data(self):
        # does not need to be converted to correct point geometry, already
        #correct
        self.cities = gpd.read_file('data/cities.geojson')

        # rp(self.cities)
        # Convert to dataframe later
        self.ufo = pd.read_csv('data/BetterUFO.csv')
        self.boundary = gpd.read_file('data/us_border_shp/us_border.shp')
        self.borders = gpd.read_file("data/us_borders.geojson")
        fig, ax = plt.subplots(figsize=(12, 10))
        self.borders.plot(ax=ax, color='blue')
        self.ufo = geopandas.GeoDataFrame(
            self.ufo,
            geometry=geopandas.points_from_xy(
                        self.ufo.lon,
                        self.ufo.lat))





        self.border_proj = self.cities.to_crs(self.boundary.crs)
        self.border_proj.name='US Boundaries'
        self.boundary_shape = unary_union(self.boundary.geometry)
        coordinates = points_to_coords(self.border_proj.geometry)
        voronoi_regions_from_coords(coordinates, self.boundary_shape)
        region_polys, region_pts = voronoi_regions_from_coords(
            coordinates,
            self.boundary_shape)
        # for i, poly in region_polys.items():
        #     print(i)
        #     print(poly)
        plot_voronoi_polys_with_points_in_area(ax,
                                               self.boundary_shape,
                                               region_polys,
                                               coordinates,
                                               region_pts)
        self.cities.plot(ax=ax, color='gray', markersize=5.5)
        rp(self.cities)
        self.ufo.plot(ax=ax, color='green', markersize=.3)
        ax.axis('off')
        plt.axis('equal')
        minx, miny, maxx, maxy = self.boundary.total_bounds
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)

        #plt.show()


        reg_poly_len = len(region_polys)
        point_begin = reg_poly_len
        ufo_point_dict = dict()
        for point in list(self.ufo.values):
            region_polys.update({point_begin : point[7]})
            # rp(region_polys[point_begin])
            ufo_point_dict[point_begin] = point[7]
            point_begin += 1

        rtree = geopandas.GeoSeries(region_polys)
        index = 0
        self.ufo.set_crs(epsg=4326, inplace=True)
        # dfout = gpd.sjoin(self.cities, self.ufo, how="inner",
        #                   predicate="within")
        output = []
        polypoints = []
        type_of = 'Oops'
        for i in range(0, reg_poly_len):
            if (type(rtree[i]) == Polygon):
                type_of = 'Single'
                polypoints = list(rtree[i].exterior.coords)
                print(rtree[i].exterior.coords)
            elif type(rtree[i]) == MultiPolygon:
                type_of = 'Multi'
                polypoints = []
                for polygon in rtree[i]:
                    coords = numpy.asarray(polygon.exterior.coords)
                    coords = coords.tolist()
                    polypoints.append(coords)

            query = rtree.sindex.query(rtree[i])

            points =[]
            for point in query:
                if type(rtree[point]) == shapely.geometry.point.Point:
                    # print(rtree[point].x)
                    # print(rtree[point].y)
                    points.append([rtree[point].x, rtree[point].y])
                    print()
            output.append({
                'type': type_of,
                'poly': polypoints,
                'points': points
            })
        with open('PolyPoints.json', 'w') as file:
            file.write(json.dumps(output))

        # print(type(rtree))
iwt = IWantToBelieve2()
iwt.load_data()


import json
import math
import os
import sys
import geopandas
import numpy
from rich import print as rp
import shapely
from shapely.geometry import Polygon, LineString, Point
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import pyproj

class GeoHelper():
    def __init__(self):
        self.country_names: list = list()
        self.polygons: dict = dict()
        self.country_data: list = list()
        self.poly_count: int = 0
        self.country_continent_frame = pd.read_csv('continents.csv')
    def load_county_data(self, file_name):
        cwd = os.getcwd()
        print(cwd)
        print(cwd)
        if os.path.isfile(file_name):
            print('yup')
            with open(file_name) as file_data:
                self.country_data = json.load(file_data)
        else:
            rp(f'Filename {file_name} is not a file.')
            sys.exit()
        if 'features' in self.country_data:
            self.country_data = self.country_data['features']
        else:
            print('WTF!?!')
            sys.exit()
    def load_country_polygons(self):
        self.poly_count = 0
        for country in self.country_data:
            name = country['properties']['name']
            self.country_names.append(name)
            self.polygons[name] = []



            for poly in country['geometry']['coordinates']:
                if len(poly) == 1:

                    self.polygons[name].append({
                        "name": name,
                        "id" : self.poly_count,
                        'coordinates' : poly[0]
                    })

                    self.poly_count = self.poly_count + 1
                else:

                    for single_poly in poly:
                        self.polygons[name].append({
                            "name": name,
                            "id" : self.poly_count,
                            "coordinates": single_poly
                        })
                        self.poly_count = self.poly_count + 1


    def get_country_index(self, name):
        if name in self.country_names:
            return self.country_names.index(name)
        else:
            return None
    def get_country_by_id(self, index):
        for country, polys in self.polygons.items():
            for polygon in polys:
                if polygon["id"] == index:
                    return country
    def get_raw_polygons(self, country):
        if country == None:
            return None
        for key, value in self.polygons.items():
            if key == country:
                return value
    def get_country_by_spatial_result(self, spatial_result):
        results = []
        ids = []
        for i in range(len(spatial_result)):
            ids.append(i)
        for country, polys in self.polygons.items():
            if polys["id"] in ids:
                results.append(polys["id"])
        return results
    def get_geo_polygons(self):
        results = []
        for _, polys in self.polygons.items():
            for poly in polys:
                results.append(Polygon(poly['coordinates']))
        return results
    def build_geo_json(self, names, outname):
        results = {"type": "FeatureCollection", "features": []}
        for name in names:
            for country in self.country_data:
                if country['properties']['name'] == name:
                    results['features'].append(country)
        with open(outname, 'w') as f:
            json.dump(results, f, indent=4)
    def get_center_point(self, name):
        coordinates = []
        data_frame = pd.read_csv('countries.csv')
        data_frame.drop(['ISO', 'COUNTRYAFF', 'AFF_ISO'], axis=1, inplace=True)
        XVal = None
        YVal = None
        for i in range(len(data_frame.COUNTRY)):

            if name == data_frame['COUNTRY'][i]:
                print('yes')
                print(data_frame['COUNTRY'][i])
                XVal = data_frame['longitude'][i]
                YVal = data_frame['latitude'][i]
                coordinates.append((XVal, YVal))
        return (XVal, YVal)
    def get_continent_by_country(self, name):
        
        continent = list()
        for i in range(len(self.country_continent_frame.Country)):
            if name == self.country_continent_frame.Country[i]:
                return self.country_continent_frame.Continent[i]
    def get_countries_by_continent(self, continent):
        country_list = list()
        for i in range(len(self.country_continent_frame.Continent)):
            if continent == self.country_continent_frame.Continent[i]:
                print(self.country_continent_frame.Country[i])
    def calculate_distance(self, country0, country1):
        country_distance =[]
        country_distance.append(country0)
        country_distance.append(country1)
        for (x1, y1), (x2, y2) in zip(country_distance, country_distance[1:]):
            distance = self.haversine(x1, y1, x2, y2)
            print(distance)

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Source:https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r
    def calculate_bearing(self, country0, country1):
        #source https://stackoverflow.com/questions/54873868/python-calculate-bearing-between-two-lat-long
        country_distance = list()
        country_distance.append(country0)
        country_distance.append(country1)

        for (x1, y1), (x2, y2) in zip(country_distance, country_distance[1:]):
            dlon = y2 - y1
            x = math.cos(math.radians(x1)) * math.sin(math.radians(dlon))
            y = math.cos(math.radians(x1)) * math.sin(
                math.radians(x2)) - math.sin(math.radians(x1)) * math.cos(
                math.radians(x2)) * math.cos(math.radians(dlon))
            brng = numpy.arctan2(x, y)
            brng = numpy.degrees(brng)
            brng = self.degToCompass(brng)
            return brng

    def degToCompass(self,num):
        #source https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words
        val = int((num / 22.5) + .5)
        arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW",
               "SW", "WSW", "W", "WNW", "NW", "NNW"]

        return arr[(val % 16)]


class SpatialIndexHelper:
    def __init__(self):
        self.spi = geopandas.GeoSeries()
    def point_in_polygon(self, point):
        result = self.spi.containsOutPutFile.geojson(Point(point[0], point[1]))
        return result
    def polygon_touches(self, polygon):
        result = self.spi.overlaps(Polygon(polygon))
        return result
    def line_interssects(self, line):
        result = self.spi.interssects(LineString(line))
        return result
    def within_polygon(self, poly):
        result = self.spi.within(Polygon(poly))
        return result
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gh = GeoHelper()

    gh.load_county_data('countries.geojson')
    gh.load_country_polygons()
    # print(gh.get_continent_by_country('China'))
    france = gh.get_center_point('France')
    germany = gh.get_center_point('Germany')

    gh.calculate_distance(france, germany)
    brng = gh.calculate_bearing(france, germany)
    print(f'Bearing is {brng}')
    #gh.get_countries_by_continent('Asia')
    # print(gh.get_country_index('Tonga'))
    # print(gh.get_raw_polygons('Tonga'))



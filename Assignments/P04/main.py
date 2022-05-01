'''
@Name:              Buddy Smith
@Assignment:        P04
@Description:       This program creates a helper module to help facilitate
@                   P06 functions for P05's api usage.
'''


import json
import math
import os
import sys

import numpy
from rich import print as rp

from shapely.geometry import Polygon, LineString, Point
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from pprint import pprint

class GeoHelper():
    '''
    @Class:             GeoHelper
    @Description:       A geojson helper class built to help the api return
    @                   correct information.
    @Data Members:      country_names:  List of country names
    @                   polygons: a dictionary to contain country polygons
    @                   poly_count: used to load country polygons
    '''
    def __init__(self):
        self.country_names: list = list()
        self.polygons: dict = dict()
        self.country_data: list = list()
        self.poly_count: int = 0
        self.country_continent_frame = pd.read_csv('continents.csv')

    def load_county_data(self, file_name):
        cwd = os.getcwd()
        if os.path.isfile(file_name):
            with open(file_name) as file_data:
                self.country_data = json.load(file_data)
        else:
            rp(f'Filename {file_name} is not a file.')
            sys.exit()
        if 'features' in self.country_data:

            self.country_data = self.country_data['features']
        else:
            sys.exit()
    def load_country_polygons(self):
        self.poly_count = 0
        for country in self.country_data:
            name = country['properties']['name']
            self.country_names.append(name)
            # create entrty polygons['name']
            self.polygons[name] = []
            for poly in country['geometry']['coordinates']:
                # print(f'{name}= {len(poly)}')
                if len(poly) == 1:
                    self.polygons[name].append({
                        "id" : self.poly_count,
                        'coordinates' : poly[0]
                    })
                    self.poly_count = self.poly_count + 1
                else:
                    for single_poly in poly:
                        self.polygons[name].append({
                            "id" : self.poly_count,
                            "coordinates": single_poly
                        })
                        self.poly_count = self.poly_count + 1
                # print(self.polygons[name])

    def load_country_names(self):
        for country in self.country_data:
            name = country['properties']['name']
            self.country_names.append(name)
    def get_country_names(self):
        return self.country_names

    def get_raw_polygons(self, country):
        if country == None:
            return None
        for key, value in self.polygons.items():
            if key == country:
                return value

    def get_geo_polygons(self):
        results = []
        for key, polys in self.polygons.items():
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

                # print(data_frame['COUNTRY'][i])
                XVal = data_frame['longitude'][i]
                YVal = data_frame['latitude'][i]
                coordinates.append((XVal, YVal))
        return (XVal, YVal)
    def get_continent_by_country(self, name):
        continent = list()
        for i in range(len(self.country_continent_frame.Country)):
            # print(self.country_continent_frame.Country[i])
            if name == self.country_continent_frame.Country[i]:
                return self.country_continent_frame.Continent[i]
    def get_countries_by_continent(self, continent):
        country_list = list()
        for i in range(len(self.country_continent_frame.Continent)):
            if continent == self.country_continent_frame.Continent[i]:
                country_list.append(self.country_continent_frame.Country[i])
        return country_list
    def calculate_distance(self, country0, country1):

        country_distance =[]
        country_distance.append(country0)
        country_distance.append(country1)
        min = 100000
        for (x1, y1), (x2, y2) in zip(country_distance, country_distance[1:]):
            distance = self.haversine(x1, y1, x2, y2)
            if distance < min:
                min = distance
        return min

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
        country_distance = []  # create and empty list
        country_distance.append(
            country0)  # append the values of the center point
        country_distance.append(
            country1)  # append the center point values to  the distance list
        for (x1, y1), (x2, y2) in zip(country_distance, country_distance[
                                                       1:]):  # zip these into one list
            # print(x1,  x2, y1, y2)
            country_direction ="Secret"
            # create some if statements to handle positioning
            if x1 < x2 and y1 > y2:
                country_direction = 'NorthWest'  # located northwest
            elif x1 > x2 and y1 > y2:
                country_direction = 'NorthEast'  # located northeast
            elif x1 < x2 and y1 < y2:
                country_direction = 'SouthWest'  # country is located to the
                # southwest
            elif x1 > x2 and y1 < y2:
                country_direction = 'SouthEast'  # country located to south
                # east
            # if none of these conditions met, then
            else:
                if x1 == x2 and y1 > y2:
                    country_direction = 'North'  # country is to the  north
                elif x1 == x2 and y1 < y2:
                    country_direction = 'South'  # country is to the south
                elif x1 < x2 and y1 == y2:
                    country_direction = 'East'  # country is to the easst
                elif x1 > x2 and y1 == y2:
                    country_direction = 'West'  # country is to the west
        return country_direction

    def degToCompass(self,num):
        #source https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words
        val = int((num / 22.5) + .5)
        arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW",
               "SW", "WSW", "W", "WNW", "NW", "NNW"]

        return arr[(val % 16)]



    def OutPutGeojson(self, name):
        for item in self.country_data:
            if item['properties']['name'] == name:

                coordinates = item['geometry']['coordinates']
                if item['geometry']['type'] == "Polygon":
                    output = {
                            "type": "FeatureCollection",
                            "features": []}
                    output['features'].append({
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates":
                                coordinates
                        }
                    })
                else:

                    output = {
                            "type": "FeatureCollection",
                            "features": []}
                    output['features'].append({
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "MultiPolygon",
                            "coordinates":
                                coordinates  #
                        }
                    })
        writer = open('output.txt','w')
        writer.write(json.dumps(output, indent=4))

        return output


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gh = GeoHelper()

    gh.load_county_data('countries.geojson')
    gh.load_country_polygons()
    gh.load_country_names()
    print(gh.get_raw_polygons('Afghanistan'))


    mexico = gh.get_center_point('Mexico')

    germany = gh.get_center_point('Germany')
    print(gh.calculate_distance(mexico, germany))
    print(gh.calculate_bearing(mexico, germany))
    print(gh.get_continent_by_country('France'))
    print(gh.get_countries_by_continent('Africa'))
    print(gh.get_raw_polygons('France'))

    print(gh.get_country_names())
    pprint(gh.OutPutGeojson('Venezuela'), indent=2)

'''
Name:               Buddy Smith
Assignment          P02
Description:        Rtree nearest neighbor with ufos. We calculate the distance
                    from each city to every other city. We return the
                    distance to the average distance to the 100 closest
                    ufos. These are wrote to avg_ufos.json
'''

import copy
import csv
import json


from pprint import pprint
import geopandas
from statistics import mean
from shapely.geometry import Point

from pydantic import BaseModel, parse_obj_as
from pydantic.typing import List
class AvgUfo(BaseModel):
    '''
    class:              AvgUfo
    members:            city: string
                        latitude: float
                        longitude: float
                        avg_ufo: float
    description:        used to writing output to file
    '''
    city: str
    latitude: float
    longitude: float
    avg_ufo: float

class IWantToBelieve:
    '''
    class:              IWantToBelieve
    members:            temp_city_name -> list
                        temp_pts -> list
                        cities -> dictionary
                        ufo_list -> list
                        ufo_pts -> list
    methods:            constructor
                        read_cities(self, file_name, debug=False)
                        read_ufo_data(self, csv_file, debug=False)
                        parse_city_info(self, debug=False)
                        setup_geopandas(self, debug=False)
    description         if debug=True is passed, pertinent info related to
                        the function is written to file, see methods for
                        locations. We calculate the distance from city to city.
                        We then query these locations using the ufo points
                        provided and determine the closest 100 ufo points.
                        then the average is taken and the information is
                        written to avg_ufo.json.  Distances are written to
                        distances.json
    '''
    def __init__(self):
        """
        Name: None -> Constructor
        """

        self.temp_city_name:list = list()
        self.temp_pts:list  = list()
        self.geo = None
        self.cities: dict = dict()
        self.cities_list: list = list()
        self.ufo_list: list = list()
        self.ufo_pts: list = list()


    def read_cities(self, file_name, debug=False):
        # read city data related to program
        with open(file_name) as cities:
            self.cities = json.load(cities)
        if debug:
            with open('debug/city_list_debug.json', 'w') as f:
                f.write(json.dumps(self.cities, indent=4))


    def read_ufo_data(self, csv_file, debug=False):
        # read ufo data related to program
        # NOTE: W.A.S. related to ufo_list, had to deep_copy, no idea why.
        with open(csv_file) as ufo_data:
            temp = list(csv.DictReader(ufo_data, delimiter=','))
            self.ufo_list = copy.deepcopy(temp)

            if debug:
                with open('debug/ufo_list_debug.json', 'w') as f:
                    f.write(json.dumps(self.ufo_list, indent=4))
    def parse_city_info(self, debug=False):
        '''
        function:           parse_city_info
        parameters:         debug -> default false
        description:        city information is iterated through, each point is
                            appended to the temp_pts list, each name is
                            added to the temp_city_names list. The cities_list
                            is appended with a POINT object representing
                            each coordinates. See if debug statements for
                            file locations related to debugging.
        '''
        for item in self.cities['features']:
            #if type equals point, appnend coordinates
            if item['geometry']['type'] == 'Point':
                # ITEM EXAMPLE
                #{'type': 'Feature',
                # 'properties': {
                #   'city': 'Portland',
                #   'growth': 15,
                #   'population': 609456,
                #   'rank': 29,
                #   'state': 'Oregon',
                #   'marker-color': '#879CB9',
                #   'marker-size': 'medium'},
                #   'geometry': {
                #       'type': 'Point',
                #       'coordinates': [-122.676482, 45.523062]}}

                # append points
                self.temp_pts.append(item['geometry']['coordinates'])
                # append city name
                self.temp_city_name.append(item['properties']['city'])
        for pnt in self.temp_pts:
            #for each pint iniside of the data point, append Point to list
            # of cities
            self.cities_list.append(Point(pnt))
        if debug:
            with open('debug/temp_city.txt', 'w') as f:
                for city in self.temp_city_name:
                    f.write(str(city) + '\n')
            with open('debug/point_list_debug.txt', 'w') as f:
                for item in self.cities_list:
                    # print(str(item))
                    f.write(str(item) + '\n')

    def setup_geopandas(self, debug=False):
        '''
        method:         setup_geopandas
        parameters:     debug ->defaulted to false
        description:    calculate the distance from each city to city using a
                        geoseries tree.The distances are then sorted and
                        written in json format to distances.json
        '''
        # create geoseries object passing list of points from cities_list
        self.geo = geopandas.GeoSeries(self.cities_list)
        output = []
        
        for x in range(len(self.geo)):
            print(self.geo[x])
            # iterate over every point in self.geo, create empty list to
            # hold distances
            dist = []
            #use geopandas.geoseries.distance to calculate diestance to each
            # point from each point
            geo_list= list(self.geo.distance(self.geo[x]))
            print(f'GEO_LIST={geo_list}')
            # pprint(geo_list)
            for i in range(len(geo_list)):
                if geo_list[i] != 0:
                    #append the distance if its not the city itself
                    dist.append((self.temp_city_name[i], geo_list[i]))

            dist.sort(key=lambda iterator: iterator[1])
            if debug:
                with open('debug/panda_list_debug.txt', 'a+') as f:
                    for item in geo_list:
                        f.write(str(item) + '\n')
            #create dict object with distance to every city from city
            city = {
                'city': self.temp_city_name[x],
                'longitude': self.geo[x].x,
                'latitude': self.geo[x].y,
                'distance': dist
            }

            output.append(city)
        # pprint(output, indent=4)
        with open('distances.json', 'w') as f:
            f.write(json.dumps(output, indent=4))

    def setup_ufo_points(self, debug=False):
        '''
        method:         setup_ufo_points
        parameters:     debug -> defaulted to false
        description:    each coordinate in the ufo file is converted to a
                        point object. a geoseries object is created using
                        all ufo points. the geoseries object is then queried for
                        each city in the geo tree. the found objects are
                        sorted by distance and only the first 100 are stored.
                        the average is then calculated for each 100 and
                        stored for each city
        '''
        with open('distances.json', 'r') as reader:
            output = json.load(reader)
        result = list()
        #iterate through list of ufo data append lat/long to ufo_pts
        for items in self.ufo_list:
            self.ufo_pts.append(
                Point(
                    float(items['lon']),
                    float(items['lat'])
                )
            )
        #create geoseries using ufo_pts
        ufo_geo = geopandas.GeoSeries(self.ufo_pts)
        for i in range(len(self.geo)):
            print(self.geo[i])
            dist_list = list(ufo_geo.distance(self.geo[i]))
            dist_list = sorted(dist_list, key=lambda x: float(x))
            closest_100 = dist_list[0:100]
            avg_dst = mean(closest_100)


            avg_city = {
                'city': str(output[i]['city']),
                'latitude': float(self.geo[i].x),
                'longitude': float(self.geo[i].y),
                'avg_ufo': float(round(avg_dst, 5))
            }
            print(avg_city)
            result.append(avg_city)
        if debug:
            pprint(result, indent=5)
        m = parse_obj_as(List[AvgUfo], result)
        with open('avg_ufo.json', 'w') as writer:
            writer.write(json.dumps(result, indent=4))


if __name__ == '__main__':
    iwtb = IWantToBelieve()

    iwtb.read_cities('data/cities.geojson', True)

    iwtb.read_ufo_data('data/ufo_data.csv', True)
    #
    iwtb.parse_city_info(True)
    iwtb.setup_geopandas(True)
    iwtb.setup_ufo_points()


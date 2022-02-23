import copy
import csv
import json
import pickle
import sys
from pprint import pprint
import geopandas
from statistics import mean
from shapely.geometry import Point, LineString, Polygon
import pydantic
from pydantic import BaseModel, parse_obj_as
from pydantic.typing import List
class AvgUfo(BaseModel):
    city: str
    latitude: float
    longitude: float
    avg_ufo: float

class IWantToBelieve:
    def __init__(self):
        self.temp_city_name:list = list()
        self.temp_pts:list  = list()
        self.geo = None
        self.cities: dict = dict()
        self.cities_list: list = list()
        self.ufo_list: list = list()
        self.ufo_pts: list = list()


    def read_cities(self, file_name, debug=False):
        with open(file_name) as cities:
            self.cities = json.load(cities)
        if debug:
            with open('debug/city_list_debug.json', 'w') as f:
                f.write(json.dumps(self.cities, indent=4))



    def read_ufo_data(self, csv_file, debug=False):
        with open(csv_file) as ufo_data:
            temp = list(csv.DictReader(ufo_data, delimiter=','))
            self.ufo_list = copy.deepcopy(temp)
            # for row in temp:
            #     self.ufo_list.append(row)
            if debug:
                with open('debug/ufo_list_debug.json', 'w') as f:
                    f.write(json.dumps(self.ufo_list, indent=4))
    def parse_city_info(self, debug=False):
        for item in self.cities['features']:
            if item['geometry']['type'] == 'Point':
                self.temp_pts.append(item['geometry']['coordinates'])
                self.temp_city_name.append(item['properties']['city'])
        for pnt in self.temp_pts:
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
        self.geo = geopandas.GeoSeries(self.cities_list)
        output = []
        
        for x in range(len(self.geo)):
            dist = []

            geo_list= list(self.geo.distance(self.geo[x]))
            # pprint(self.geo[x])
            for i in range(len(geo_list)):
                if geo_list[i] != 0:
                    dist.append((self.temp_city_name[i], geo_list[i]))

            dist.sort(key=lambda x: x[1])
            if debug:
                with open('debug/panda_list_debug.txt', 'a+') as f:
                    for item in geo_list:
                        f.write(str(item) + '\n')

            city = {
                'city': self.temp_city_name[x],
                'longitude': self.geo[i].x,
                'latitude': self.geo[i].y,
                'distance': dist
            }

            output.append(city)
        # pprint(output, indent=4)
        with open('distances.json', 'w') as f:
            f.write(json.dumps(output, indent=4))

    def setup_ufo_points(self, debug=False):
        with open('distances.json', 'r') as reader:
            output = json.load(reader)
        result: list = list()
        for items in self.ufo_list:
            self.ufo_pts.append(
                Point(
                    float(items['lon']),
                    float(items['lat'])
                )
            )
        ufo_geo = geopandas.GeoSeries(self.ufo_pts)
        for i in range(len(self.geo)):
            distance = []
            #print(self.geo[i])
            dist_list = list(ufo_geo.distance(self.geo[i]))
            dist_list = sorted(dist_list, key=lambda x: float(x))
            closest_100 = dist_list[0:100]
            avg_dst = mean(closest_100)
            #pprint(dist_list, indent=4) if debug else ...

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

        # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    iwtb = IWantToBelieve()

    iwtb.read_cities('data/cities.geojson', True)

    iwtb.read_ufo_data('data/ufo_data.csv', True)
    #
    iwtb.parse_city_info(True)
    iwtb.setup_geopandas(True)
    iwtb.setup_ufo_points()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

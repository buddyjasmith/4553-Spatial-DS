import os

import geopandas
import json
from pprint import pprint
from shapely.geometry import Point
import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
class P08:
    def __init__(self):
        self.header = None
        self.states = None
        with open('states.geojson') as data:
            self.states = geopandas.read_file(data)
        self.cities = None
        with open('cities.json') as data:
            self.cities = json.load(data)
        self.city_frame = None
        self.states_json = None
        with open('states.geojson') as data:
            self.states_json = json.load(data)
        self.states_json = self.states_json['features']
        self.states_dict = {}

    def get_city_color(self, population):
        '''
        @params: population -> number
        @description: returns a hex color based upon the size of population
        '''
        if population < 30000:
            return '#EEF6FF'
        elif population < 40000:
            return '#CCE4FF'
        elif population < 50000:
            return '#AAD2FF'
        elif population < 60000:
            return '#88C0FF'
        elif population < 70000:
            return '#66AEFF'
        elif population < 80000:
            return '#449CFF'
        elif population < 100000:
            return '#228AFF'
        elif population < 120000:
            return '#0078FF'
        elif population < 150000:
            return '#0068DD'
        elif population < 200000:
            return '#0058BB'
        elif population < 250000:
            return '#004899'
        elif population < 300000:
            return '#003877'
        else:
            return '#001833'
    def get_color(self, population):
        '''
        @params: population -> number
        @description: returns a hex color based upon the size of population
        '''
        if population < 100000:
            return '#ffffff'
        elif population < 250000:
            return '#ffe6e6'
        elif population < 500000:
            return '#ffcccc'
        elif population < 1000000:
            return '#ffb3b3'
        elif population < 2000000:
            return '#ff9999'
        elif population < 3000000:
            return '#ff8080'
        elif population < 4000000:
            return '#ff6666'
        elif population < 5000000:
            return '#ff4d4d'
        elif population < 6000000:
            return '#ff3333'
        elif population < 7000000:
            return '#ff1a1a'
        elif population < 8000000:
            return '#ff0000'
        elif population < 9000000:
            return '#e60000'
        elif population < 10000000:
            return '#cc0000'
        elif population < 15000000:
            return '#b30000'
        elif population < 20000000:
            return '#990000'
        else:
            return '#000000'
    def begin(self):
        # append values to property for display later, add population to hold
        # population of the state
        for item in self.states_json:
            item['properties']['population'] = 0
            item['properties']['title'] = item['properties']['name']
            # item['properties']['stroke'] = "#555555"
            item['properties']['stroke-width'] = 1
            item['properties']['fill'] = '#ffffff'

            pprint(item, indent=2)
        for item in self.states_json:
            self.states_dict[item['properties']['name']] = 0
        state_tree = geopandas.GeoSeries(self.states['geometry'])
        for i in range(len(self.cities)):
            temp_pnt = Point(
                self.cities[i]['longitude'],
                self.cities[i]['latitude'])
            query = state_tree.sindex.query(temp_pnt, predicate='within')
            if query.size == 1:
                # represents the number of the feature in the feature
                # collection
                temp_num = query.item(0)
                # print(self.states_json[temp_num])
                # print(f'Coordinates {temp_pnt} found within '
                #       f"{self.states_json[temp_num]['properties']['name']} "
                #       f"with a population of {self.cities[i]['population']}")
                self.states_dict[self.states_json[temp_num]['properties'] \
                    ['name']] += self.cities[i]['population']
            elif query.size > 1:
                print("We aren't in Kansas anymore")
            elif query.size == 0:
                print('No matches for for query')

        for k, v in self.states_dict.items():
            # set name, population, and color in states_json
            for item in self.states_json:
                if item['properties']['name'] == k:
                    item['properties']['population'] = v
                    item['properties']['fill'] = self.get_color(
                        item['properties']['population'])
                    print(item)

        self.header = {
            "type": "FeatureCollection",
            "features": []}
        for item in self.states_json:
            self.header['features'].append(item)
        # with open('output.txt', 'w') as writer:
        #     writer.write(json.dumps(self.header, indent=4))
    def fix_cities(self):

        for item in self.cities:
            print(item)
            temp_dict = {
                "type": "Feature",
                "properties":{
                    "fill": self.get_city_color(item['population']),
                    "population": item['population']
                },
                "geometry":{
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [item['longitude'] + .1, item['latitude']],

                            [item['longitude'], item['latitude']+.1],
                            [item['longitude'] - .1, item['latitude']],
                            [item['longitude'], item['latitude']-.1],
                            [item['longitude'] + .1, item['latitude']],
                        ]
                    ]
                }

            }
            self.header['features'].append(temp_dict)

        with open('output.txt', 'w') as writer:
            writer.write(json.dumps(self.header, indent=4))




p08 = P08()
p08.begin()
p08.fix_cities()

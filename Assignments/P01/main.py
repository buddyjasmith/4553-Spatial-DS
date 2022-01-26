'''
:author:        Buddy Smith
:assignment:    P01
:date:          01/25/2022
:description:   Json data is converted to GeoJson format.  Each city in the US
:               is ranked by population in conjunction with the state.  The
:               Geojson object is plotted and connected from west to east.
:               The route is not effecient.
'''
import json
import random
from rich import print
from rich import console

class EastWest:
    '''
    :class:                EastWest
    :var -> self.states:   holds state[cities_data]
    :var -> self.max_population_centers: holds the largest cities in each state
    :var -> ranked_cities: at different points holds the cities in each state
    :                      by population, and then sorted from west to east
    :var -> self.geo_list: holds the end product, the geojson object of
    :                      completed work
    :var -> self.console:  rich.console library used for pretty printing
    :methods:
    :random_generator(): returns a random RGB value, ie. #ABC in a tuple object
    :read_json_data():   reads supplied json data from file and converts to
    :                    a dictionary
    :filter_cities():    removes entries hawaii and alaska from data fields
    :rank_cities():      city_data is ranked by population and each object
    :                    is appended self.ranked_cities for plotting usage
    :convert_to_GeoJson: this is the main function. ranked cities are built
    :                    into a geojson object.  lines are added from east to
    :                    west
    '''
    def __init__(self):
        self.states = {}
        self.max_population_centers = {}
        self.ranked_cities = []
        self.geo_list = []
        self.console = console.Console()

    def random_generator(self):
        r = random.choice(
            [random.choice('ABCDEF0123456789') for i in range(6)])
        g = random.choice(
            [random.choice('ABCDEF0123456789') for i in range(6)])
        b = random.choice(
            [random.choice('ABCDEF0123456789') for i in range(6)])
        return f'#{r}{g}{b}'
        return (r, g, b)

    def read_json_data(self):
        '''
        :raises:        EnvironmentError: parent of IOError, OSError, etc
        :description:   cities.json is open and loaded into the scoped variable
        :               city_data.  from this point each entry is broken down
        :               by state and stored in self.states
        '''
        try:
            with open('cities.json') as data:
                city_data = json.load(data)
        except EnvironmentError as e:
            print(f'An error occured of type {e}')
        for city in city_data:
            if not city['state'] in self.states:
                state = city['state']
                self.states[state] = []
            self.states[city['state']].append(city)

    def filter_cities(self):
        '''
        :var state:       represents the state stored in self.states key entry
        :var city_list:   city information stored as a dicitonary
        :description:     cities must be below 110 longitude, less the 50
        :                 latitude and greater than 25 latitude.  Simply put
        :                 we filter out Alaska and Hawaii.
        '''
        for state, city_list in self.states.items():
            max = -1
            for entry in city_list:
                if entry['population'] > max and entry['longitude'] < 110 \
                        and entry['latitude'] < 50 and entry['latitude'] > 25:
                    max = int(entry['population'])
                    self.max_population_centers[state] = entry
            # for entry, value in self.max_population_centers.items():
            #     print(entry, value)

    def rank_cities(self):
        '''
        :param -> None
        :return -> None
        :description -> the city data belonging to max_population_centers
        :               is added to the list ranked cities. This list is then
        :               sorted by population. The population ranking is then
        :               used as a marker on the map
        :important ->   The ranking index uses 1 as the smallest index and the
        :               largest index will represent the greater population
        :               centers
        '''
        ''''''
        for key, value in self.max_population_centers.items():
            self.ranked_cities.append(value)

        # Sort ranked cities by population, this will allow us to use the
        # ranking as the marker for GeoJson
        self.ranked_cities = sorted(self.ranked_cities,
                                    key=lambda d: d['population'])

        # Set the ranking of the Cities, will begin at 1 being the smallest
        num = 1
        for item in self.ranked_cities:
            item['rank'] = num
            num += 1
        self.console.print(self.ranked_cities, style="black on white")

    def convert_to_geojson(self):
        '''
        :param -> None
        :var -> city_data: represent a city json object in ranked cities
        :description -> Create a Larger Geojson object, set the color, size,
        :               and marker symbol to be used on the map.  Append the
        :               city data info to rankedcites['properties'] field.
        :               Ranked cities is then sorted from West to east and
        :               LineStrings are appended to the geolist from west to
        :               east.
        '''
        self.geo_list = {
            "type": "FeatureCollection",
            "features": []
        }
        for city_data in self.ranked_cities:
            city_data['marker-color'] = self.random_generator()
            city_data['marker-size'] = "medium"
            city_data['marker-symbol'] = city_data['rank']

            self.geo_list['features'].append({
                "type": "Feature",
                "properties": city_data,
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        city_data['longitude'],
                        city_data['latitude'],
                    ]}})
        # Sort from west to east, by longitude
        self.ranked_cities = sorted(self.ranked_cities,
                                    key=lambda d: d['longitude'])
        print(self.ranked_cities)
        # add LineStrings between cooordinates, since sorted by longitude add
        # lines between ranked_cites[i] and ranked_cities[i+1] from west to
        # east
        for i in range(len(self.ranked_cities)):
            if_i = i+1 if i is not (len(self.ranked_cities) - 1) else i
            self.geo_list['features'].append(
                {
                    "type": "Feature",
                    "properties":{
                        "stroke": self.random_generator(),
                        "stroke-width": 2,
                    },
                    "geometry":{
                        "type": "LineString",
                        "coordinates":[
                            [self.ranked_cities[i]['longitude'],
                            self.ranked_cities[i]['latitude']],
                            [self.ranked_cities[if_i]['longitude'],
                             self.ranked_cities[if_i]['latitude']],
                        ]
                    }
                }
            )
        with open('outputfile.json', 'w') as file:
            file.write(json.dumps(self.geo_list, indent=4))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ew = EastWest()
    ew.read_json_data()
    ew.filter_cities()
    ew.rank_cities()
    ew.convert_to_geojson()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

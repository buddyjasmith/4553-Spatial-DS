

import json  # json data
import pandas as pd
import math  # for math calculation
import sys
class Geography:
    def __init__(self):  # working
        try:
            with open('countries.geojson') as infile:
                self.DataWorld = json.load(infile)
        except IOError:
            print('Wrong File name given')
            sys.exit()
        try:
            self.output = open('OutPutFile.geojson', 'w')
        except IOError:
            print("there was an issue creating the output file\n")

    def getCountryList(self):  # working
        DictList = []
        for feature in self.DataWorld['features']:
            DictList.append(
                feature['properties']['name'])
        return (
            DictList)

    def getPolyGon(self, name):  # working
        for feature in self.DataWorld['features']:
            if (feature['properties']['name'] == name):
                print("The name of the country is : ", name,
                      " the coordinates are :\n\n", feature['geometry'][
                          'coordinates'])
            coordinates = feature['geometry']['coordinates']
            return coordinates

    def GetCenterPoint(self, name):
        coordinate = []
        df1 = pd.read_csv('Assignments/P04/countries.csv')
        df1.drop(['ISO', 'COUNTRYAFF', 'AFF_ISO'], axis=1, inplace=True)
        XVal = None
        YVal = None
        for i in range(len(df1.COUNTRY)):
            if name == df1['COUNTRY'][i]:
                XVal = df1['longitude'][i]
                YVal = df1['latitude'][i]
                coordinate.append(
                    (XVal, YVal))

        return XVal, YVal

    # returning the country to the user read in the data name and return the continent it islocated on
    def GetContinent(self, name):
        continent = None
        df2 = pd.read_csv(
            'Assignments/P04/continents.csv')
        for i in range(
                len(df2.Country)):
            if name == df2['Country'][i]:
                continent = df2['Continent'][i]
        return continent


    def CalculateDistance(self, Country1, Country2):
        CountryDist = []
        CountryDist.append(Country1)
        CountryDist.append(Country2)
        DistanceValue = None
        for (x1, y1), (x2, y2) in zip(CountryDist, CountryDist[1:]):
            DistanceValue = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)



        return DistanceValue * 69

    def getDirection(self, FirstCountry, SecondCountry):

        CountryDistance = []
        CountryDistance.append(FirstCountry)
        CountryDistance.append(SecondCountry)
        for (x1, y1), (x2, y2) in zip(CountryDistance, CountryDistance[1:]):

            if x1 < x2 and y1 > y2:
                CountryDirection = 'NorthWest'
            elif x1 > x2 and y1 > y2:
                CountryDirection = 'NorthEast'
            elif x1 < x2 and y1 < y2:
                CountryDirection = 'SouthWest'
            elif x1 > x2 and y1 < y2:
                CountryDirection = 'SouthEast'
            else:
                if x1 == x2 and y1 > y2:
                    CountryDirection = 'North'
                elif x1 == x2 and y1 < y2:
                    CountryDirection = 'South'
                elif x1 < x2 and y1 == y2:
                    CountryDirection = 'East'
                elif x1 > x2 and y1 == y2:
                    CountryDirection = 'West'

        return CountryDirection

    # working geojson # plug into geojson.io
    def OutPutGeojson(self, name):
        for feature in self.DataWorld['features']:
            if (feature['properties']['name'] == name):
                print("The name of the country is : ", name,
                      " the coordinates are :\n\n", feature['geometry'][
                          'coordinates'])  # pass back the coordinate of the specified name
                coordinates = feature['geometry']['coordinates']

                OutFile = {
                    "type": "FeatureCollection",
                    "features": []
                }
                OutFile['features'].append({
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates":
                            coordinates


                    }
                })
                # write to the ouput file

                self.output.write(json.dumps(OutFile, indent=4))
                return OutFile


# loads up API
if __name__ == '__main__':
    GeoCountry = Geography()  # assign value object of the class

    #GeoCountry.getPolyGon('Yemen')  # lets get the polygon for yemen
    ## GeoCountry.CalculateCenterPoint('Yemen')
    #GeoCountry.OutPutGeojson('Yemen')  # get an output geojson file for yemen
    print(GeoCountry.GetContinent('Asia'))
    #
    # print("center is :\n\n", GeoCountry.GetCenterPoint(
    #     'Bolivia'))  # get the center point for yemen
    # print(GeoCountry.GetContinent('United States'))
    # # print(GeoCountry.CalculateDistance('Yemen','United States'))
    # Country1 = GeoCountry.GetCenterPoint('Bolivia')
    # Country2 = GeoCountry.GetCenterPoint('Brazil')
    # DistanceBetween = GeoCountry.CalculateDistance(Country1, Country2)
    # print("the distance between the countries is : \n", DistanceBetween)





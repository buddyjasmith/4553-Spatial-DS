############################################################
##                                                        ##
##                                                        ##
##  Ethan Coyle                                           ##
##  Dr. Griffin - CMPS 4551 Spatial Data Structures       ##
##  P06 - APIHelper Class o help with geo spatial data    ##
##                                                        ##
############################################################
##                                                        ##
##  The purpose of this assignment is to create helper    ##
##  classes that aid in the processing of our data file   ##
##  by using fast API to process data this is working by  ##
##  running through port 8080 by calling the main python  ##
##  as helper api and importing the class inside of the data
##                                                        ##
############################################################
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import geopandas as gdp  # for the gdp spatial data
from shapely.geometry import Polygon  # for OutPut polygons
import json  # json data
import pandas as pd
import math  # for math calculation
from fastapi.middleware.cors import CORSMiddleware  # needed for the api
from math import radians, cos, sin, asin, sqrt


# from the geohelper python import our class to be utilizes in our api
# from GeoHelper import GeoraphicData

###########################################################################################################################################
#  ██████╗██╗      █████╗ ███████╗███████╗     █████╗ ███╗   ██╗██████╗     ███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗ #
# ██╔════╝██║     ██╔══██╗██╔════╝██╔════╝    ██╔══██╗████╗  ██║██╔══██╗    ████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝ #
# ██║     ██║     ███████║███████╗███████╗    ███████║██╔██╗ ██║██║  ██║    ██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗ #
# ██║     ██║     ██╔══██║╚════██║╚════██║    ██╔══██║██║╚██╗██║██║  ██║    ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║ #
# ╚██████╗███████╗██║  ██║███████║███████║    ██║  ██║██║ ╚████║██████╔╝    ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║ #
#  ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ #
###########################################################################################################################################
class Geography:
    def __init__(self):  # working
        # for the input file try to open the file
        try:
            # try to open the inputfile
            with open('countries.geojson') as infile:
                self.DataWorld = json.load(infile)
                # clearprint(self.DataWorld)
        # if opening unsuccessful, toss an error
        except IOError:
            print('there was an error with you file')
        # add exception handling on if there is and error opening up a outputfile
        try:
            # open up and output file with the gejson format as a writeable file
            self.output = open('OutPutFile.geojson', 'w')
        except IOError:
            # if unsuccessful, throw and input output exception
            print("there was an issue creating the output file\n")

    def getCountryList(self):  # working
        DictList = []
        for feature in self.DataWorld['features']:
            # print(feature['geometry']['type'])# type of the country
            DictList.append(
                feature['properties']['name'])  # name of the country
        return (
            DictList)  # returns the dictionary list of all the country names
        # print (feature['geometry']['coordinates']) # coordinates of the country

    def getPolyGon(self, name):  # working
        for feature in self.DataWorld['features']:
            # print(feature['geometry']['type'])# type of the country
            if (feature['properties']['name'] == name):
                print("The name of the country is : ", name,
                      " the coordinates are :\n\n", feature['geometry'][
                          'coordinates'])  # pass back the coordinate of the specified name
            coordinates = feature['geometry']['coordinates']
            return coordinates

            # neeeding work

    def GetCenterPoint(self, name):  # still testing to get the center point
        coordinate = []
        df1 = pd.read_csv('countries.csv')
        # df1.drop(columns=['ISO','COUNTRYAFF','AFF_ISO']Inplace=True)
        df1.drop(['ISO', 'COUNTRYAFF', 'AFF_ISO'], axis=1, inplace=True)
        print(df1)
        # df1=df1.drop(labels='ISO','COUNTRYAFF','AFF_ISO', axis=1)
        # print(df1.head(20))
        for i in range(len(df1.COUNTRY)):  # for the length of the file
            if name == df1['COUNTRY'][i]:  # if the name matches the data name
                XVal = df1['longitude'][i]  # the lognitude is the  x coord
                YVal = df1['latitude'][i]  # lat is the y coord
                coordinate.append(
                    (XVal, YVal))  # append these values to the list
                # value= print(df1['longitude'][i],',', df1['latitude'][i])

        return XVal, YVal  # return the list with the coordinates for center point

    # returning the country to the user read in the data name and return the continent it islocated on
    def GetContinent(self, name):  # still testing to get the center point
        df2 = pd.read_csv(
            'continents.csv')  # read in the other data file
        for i in range(
                len(df2.Country)):  # for the whole length of the file checking
            if name == df2['Country'][
                i]:  # if the name match the continent in the data file,
                continent = df2['Continent'][
                    i]  # that continent is where is located
                # value= print(df2['longitude'][i],',', df2['latitude'][i])
        return continent  # return the continent name for better understanding of location

    # need distance method to work something wonkey now
    # need distance method to work something wonkey now
    def CalculateDistance(self, Country1, Country2):
        CountryDist = []
        CountryDist.append(Country1)
        CountryDist.append(Country2)
        for (x1, y1), (x2, y2) in zip(CountryDist, CountryDist[1:]):
            # convert decimal degrees to radians
            x1, y1, x2, y2 = map(radians, [x1, y1, x2, y2])
            # haversine formula
            dlon = x2 - x1
            dlat = y2 - y1
            a = sin(dlat / 2) ** 2 + cos(y1) * cos(y2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
            value = (c * r) / 1.609  # convert to miles
        return value

    # method to find the direction of the country  passing in the two countrys
    def getDirection(self, FirstCountry, SecondCountry):

        CountryDistance = []  # create and empty list
        CountryDistance.append(
            FirstCountry)  # append the values of the center point
        CountryDistance.append(
            SecondCountry)  # append the center point values to  the distance list
        for (x1, y1), (x2, y2) in zip(CountryDistance, CountryDistance[
                                                       1:]):  # zip these into one list
            # create some if statements to handle positioning
            if x1 < x2 and y1 > y2:
                CountryDirection = 'NorthWest'  # located northwest
            elif x1 > x2 and y1 > y2:
                CountryDirection = 'NorthEast'  # located northeast
            elif x1 < x2 and y1 < y2:
                CountryDirection = 'SouthWest'  # country is located to the  southwest
            elif x1 > x2 and y1 < y2:
                CountryDirection = 'SouthEast'  # country located to south east
            # if none of these conditions met, then
            else:
                if x1 == x2 and y1 > y2:
                    CountryDirection = 'North'  # country is to the  north
                elif x1 == x2 and y1 < y2:
                    CountryDirection = 'South'  # country is to the south
                elif x1 < x2 and y1 == y2:
                    CountryDirection = 'East'  # country is to the easst
                elif x1 > x2 and y1 == y2:
                    CountryDirection = 'West'  # country is to the west

        return CountryDirection  # return the country direction

    # working geojson # plug into geojson.io
    def OutPutGeojson(self, name):
        for feature in self.DataWorld['features']:
            # print(feature['geometry']['type'])# type of the country
            if (feature['properties']['name'] == name):
                print("The name of the country is : ", name,
                      " the coordinates are :\n\n", feature['geometry'][
                          'coordinates'])  # pass back the coordinate of the specified name
                coordinates = feature['geometry']['coordinates']
                # for i in range(len(coordinates)):
                #     for j in range(len(coordinates[i])):
                #         coordinates[i][j][0],coordinates[i][j][1]=coordinates[i][j][1],coordinates[i][j][0]

                if (feature['geometry']['type'] == 'Polygon'):

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
                            # append the coordinates of the coordinates to that country name

                        }
                    })
                else:
                    OutFile = {
                        "type": "FeatureCollection",
                        "features": []
                    }
                    OutFile['features'].append({
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "MultiPolygon",
                            "coordinates":
                                coordinates
                            # append the coordinates of the coordinates to that country name

                        }
                    })
                # write to the ouput file

                self.output.write(json.dumps(OutFile, indent=4))

                return OutFile


# loads up API
if __name__ == '__main__':
    uvicorn.run("main:HelperApi", host="127.0.0.1", port=8080,
                log_level="debug", reload=True)

ImportedData = Geography()  # our python helper class pushed into
##############################################################################################
#  █████╗ ██████╗ ██╗        ███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗  ##
# ██╔══██╗██╔══██╗██║        ████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝  ##
# ███████║██████╔╝██║        ██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗  ##
# ██╔══██║██╔═══╝ ██║        ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║  ##
# ██║  ██║██║     ██║        ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║  ##
# ╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝  ##
##############################################################################################
# Needed for CORS
origins = ["*"]

description = """🚀
## Worldle Clone
### With Better Distance Calculations
"""

HelperApi = FastAPI(title="Worldle Clone",
                    description=description,
                    version="0.0.1",
                    terms_of_service="http://killzonmbieswith.us/worldleterms/",
                    contact={
                        "name": "Worldle Clone",
                        "url": "http://killzonmbieswith.us/worldle/contact/",
                        "email": "chacha@killzonmbieswith.us",
                    },
                    license_info={
                        "name": "Apache 2.0",
                        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                    }, )  # getting our api running
# Needed for CORS
HelperApi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# path through the api that leads to all the doc files inside of the requester root directory
@HelperApi.get('/')
async def RootFolder():  # create a root folder for all the documents grabbed by the api
    return RedirectResponse(
        url="/docs")  # direct response to the documents folder ending in docs


##################################################################################################
#  ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗██████╗ ██╗   ██╗    ██╗     ██╗███████╗████████╗ #
# ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝    ██║     ██║██╔════╝╚══██╔══╝ #
# ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝     ██║     ██║███████╗   ██║    #
# ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝      ██║     ██║╚════██║   ██║    #
# ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   ██║  ██║   ██║       ███████╗██║███████║   ██║    #
#  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝       ╚══════╝╚═╝╚══════╝   ╚═╝    #
##################################################################################################
## use api get method to retrieve the countires
@HelperApi.get('/CountryList/')  # api helper getter to get the countries
async def countries():  # we need to give definition to the countries
    countries = ImportedData.getCountryList()  # go to the method and iterate through infile and find the countries
    OutPut = {'detail': 'Success',
              'countries': countries}  # displays list of countries from the file
    return OutPut  # return the output result


# api get feature working for below
# use get method in api to get the polygon of specified country
###############################################################
# ██████╗  ██████╗ ██╗  ██╗   ██╗ ██████╗  ██████╗ ███╗   ██╗ #
# ██╔══██╗██╔═══██╗██║  ╚██╗ ██╔╝██╔════╝ ██╔═══██╗████╗  ██║ #
# ██████╔╝██║   ██║██║   ╚████╔╝ ██║  ███╗██║   ██║██╔██╗ ██║ #
# ██╔═══╝ ██║   ██║██║    ╚██╔╝  ██║   ██║██║   ██║██║╚██╗██║ #
# ██║     ╚██████╔╝███████╗██║   ╚██████╔╝╚██████╔╝██║ ╚████║ #
# ╚═╝      ╚═════╝ ╚══════╝╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ #
###############################################################
@HelperApi.get('/FindPolyGon/{country}')
async def PolyGon(country: str):  # pass in the string of the country
    country = country.title()  # the title of the country
    country = ImportedData.getPolyGon(country)  # get the polygon
    OutPut = {
        'PolyGon for Country': country}  # if successful, display the country polygon
    return OutPut


################################################################################
#  ██████╗ ██████╗ ███╗   ██╗████████╗██╗███╗   ██╗███████╗███╗   ██╗████████╗ #
# ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝████╗  ██║╚══██╔══╝ #
# ██║     ██║   ██║██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██╔██╗ ██║   ██║    #
# ██║     ██║   ██║██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║╚██╗██║   ██║    #
# ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║██║ ╚████║███████╗██║ ╚████║   ██║    #
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝   ╚═╝    #
################################################################################
@HelperApi.get(
    '/FindContinet/{country}')  # creating the index for the continet in the api pass in the country
async def ContinentLocator(
        country: str):  # type in box for executable country finder
    Continent = ImportedData.GetContinent(
        country)  # we want the geojson file for the given country
    OutPut = {
        'Country Continent': Continent}  # if successful, pass back the center point of the country
    return OutPut  # return the result


#########################################################################################################################
#  ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗██████╗ ██╗   ██╗     ██████╗███████╗███╗   ██╗████████╗███████╗██████╗  #
# ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝    ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔══██╗ #
# ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝     ██║     █████╗  ██╔██╗ ██║   ██║   █████╗  ██████╔╝ #
# ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝      ██║     ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗ #
# ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   ██║  ██║   ██║       ╚██████╗███████╗██║ ╚████║   ██║   ███████╗██║  ██║ #
#  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝        ╚═════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ #
#########################################################################################################################
@HelperApi.get('/FindCenter/{country}')
async def Country_Center(country: str):  # type in a country name
    # country = country.title() # will look at the title and
    CountryCenter = ImportedData.GetCenterPoint(
        country)  # call the center point method
    OutPut = {
        'Country Center': CountryCenter}  # if successful, pass back the center point of the country
    return OutPut  # resturn the result


##################################################################
# ██████╗ ██╗███████╗████████╗ █████╗ ███╗   ██╗ ██████╗███████╗ #
# ██╔══██╗██║██╔════╝╚══██╔══╝██╔══██╗████╗  ██║██╔════╝██╔════╝ #
# ██║  ██║██║███████╗   ██║   ███████║██╔██╗ ██║██║     █████╗   #
# ██║  ██║██║╚════██║   ██║   ██╔══██║██║╚██╗██║██║     ██╔══╝   #
# ██████╔╝██║███████║   ██║   ██║  ██║██║ ╚████║╚██████╗███████╗ #
# ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝ #
##################################################################
## api helper to get the distance between the polygons
@HelperApi.get('/FindDistance/{FirstCountry},{SecondCountry}')
async def Country_Distance(FirstPoly: str,
                           SecondPoly: str):  # to calculate the distance inside the api use two string country polygons
    # access the two containers to get the points from each one
    Country1 = ImportedData.GetCenterPoint(FirstPoly)
    Country2 = ImportedData.GetCenterPoint(SecondPoly)
    DistanceBetween = ImportedData.CalculateDistance(Country1,
                                                     Country2)  # call the class method
    OutPut = {
        'distance': DistanceBetween}  # if successful then print out the distance
    return OutPut  # return the result


######################################################################
# ██████╗ ██╗██████╗ ███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗ #
# ██╔══██╗██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║ #
# ██║  ██║██║██████╔╝█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║ #
# ██║  ██║██║██╔══██╗██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║ #
# ██████╔╝██║██║  ██║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║ #
# ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ #
######################################################################
# create an api graber that will calculate what CountryDirection to look for the country based off the starting point
@HelperApi.get('/FindDirection/{Country1},{Country2}')
async def CountryDirection(CountryNo1: str, CountryNo2: str):
    # input the two countries calling the get centerpoint
    FirstCountry = ImportedData.GetCenterPoint(CountryNo1)
    SecondCountry = ImportedData.GetCenterPoint(CountryNo2)
    # call the method to find the distance
    DirectionToCountry = ImportedData.getDirection(FirstCountry, SecondCountry)
    # return the method back
    OutPut = {'CountryDirection': DirectionToCountry}
    return OutPut


#######################################################################################
# ████████╗ ██████╗      ██████╗ ███████╗ ██████╗      ██╗███████╗ ██████╗ ███╗   ██╗ #
# ╚══██╔══╝██╔═══██╗    ██╔════╝ ██╔════╝██╔═══██╗     ██║██╔════╝██╔═══██╗████╗  ██║ #
#    ██║   ██║   ██║    ██║  ███╗█████╗  ██║   ██║     ██║███████╗██║   ██║██╔██╗ ██║ #
#    ██║   ██║   ██║    ██║   ██║██╔══╝  ██║   ██║██   ██║╚════██║██║   ██║██║╚██╗██║ #
#    ██║   ╚██████╔╝    ╚██████╔╝███████╗╚██████╔╝╚█████╔╝███████║╚██████╔╝██║ ╚████║ #
#    ╚═╝    ╚═════╝      ╚═════╝ ╚══════╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ #
#######################################################################################

# We want to see what continet a country is located inside
@HelperApi.get(
    '/Geojson/{country}')  # creating the index for the continet in the api pass in the country
async def GeoJson(country: str):  # type in box for executable country finder
    OutPut = ImportedData.OutPutGeojson(
        country)  # we want the geojson file for the given country
    return OutPut  # return the result






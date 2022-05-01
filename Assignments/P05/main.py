'''
@Name:              Buddy Smith
@Assignment:        P05
@Description:       This program creates an api utilizing the GeoHelper class
@                   from P04, to be used in the worldle game in P06.
'''


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import json
import math

from geo_helper import GeoHelper
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# class ResponseModel(BaseModel):
#     status: str
#     details: str
#     description: str
#     results: list
geo_helper = GeoHelper()
geo_helper.load_county_data('countries.geojson')
geo_helper.load_country_polygons()

geo_api = FastAPI(
    title="Worldle Clone",
    description=None,
    version="0.0.1",

)
geo_api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@geo_api.get('/')
async def RootFolder():
    return RedirectResponse(url='/docs')

@geo_api.get('/country_names')
def get_all_country_names():
    '''
    params: None
    Return: returns a list of all country names
    '''
    return geo_helper.get_country_names()

@geo_api.get('/CountriesByContinent/{continent}')
def get_country_by_continent(continent: str):
    '''
    params: None
    Return: returns a list of all countries in a continent
    '''
    cont_list = geo_helper.get_countries_by_continent(continent)
    return cont_list

@geo_api.get('/ContinentByCountry/{country}')
def get_continent_by_country(country: str):
    '''
    params: country: string
    Return: returns the continent of a given country
    '''
    continent = geo_helper.get_continent_by_country(country)
    return continent

@geo_api.get('/country/{country}')
def get_poly_by_country(country:str):
    '''
    params: country: string
    Return: returns a polygon for a given country
    '''
    polygon = geo_helper.get_raw_polygons(country)
    return polygon

@geo_api.get('/CalculateDistance/{country0}/{country1}')
def get_distance_between_countries(country0: str, country1: str):
    '''
    params: country0: string, country1: string
    Return: calculates the distance between two countries given centers and
            returns the value in kilometers
    '''
    print(country0)
    print(country1)
    country0 = geo_helper.get_center_point(country0)
    print(country0)
    distance = None
    if country0:
        country1 = geo_helper.get_center_point(country1)
        if country1:
            distance = geo_helper.calculate_distance(country0, country1)
            print(f'DISTANCE = {distance}')
    return distance if distance else None

@geo_api.get('/CalculateBearing/{country0}/{country1}')
def calculate_bearing(country0: str, country1: str):
    '''
    params: country0: string, country1: string
    Return: calculates the bearing from country0 to country1 and returns in a
            cardinal direction format
    '''
    country0 = geo_helper.get_center_point(country0)
    country1 = geo_helper.get_center_point(country1)
    bearing = None
    if country0 and country1:
        bearing = geo_helper.calculate_bearing(country0, country1)
        print(bearing)
    return bearing

@geo_api.get('/country_names')
def get_all_countries():
    '''
    params: None
    return: list of all countries of the world
    '''
    all_countries = geo_helper.get_all_countries()
    return all_countries

@geo_api.get('/countryCenter/{country}')
def get_country_center(country: str):
    '''
    params: country: string
    Return: returns a countries given center
    '''
    center = geo_helper.get_center_point(country)
    print(center)
    return [{
        "status": 200 if center else 404,
        "details": f'Return center coordinates of {country}',
        'result': center
    }]

if __name__ == '__main__':
    uvicorn.run('main:geo_api', host='127.0.0.1', port=8080, reload=True)
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import json
import math

from geo_helper import GeoHelper
from pydantic import BaseModel

class ResponseModel(BaseModel):
    status: str
    details: str
    description: str
    results: list
geo_helper = GeoHelper()
geo_helper.load_county_data('countries.geojson')
geo_helper.load_country_polygons()

geo_api = FastAPI()

@geo_api.get('/')
async def RootFolder():
    return RedirectResponse(url='/docs')

@geo_api.get('/CountriesByContinent/{continent}')
def get_all_countries(continent: str):
    cont_list = geo_helper.get_countries_by_continent(continent)
    return cont_list

@geo_api.get('/ContinentByCountry/{country}')
def get_continent_by_country(country: str):
    continent = geo_helper.get_continent_by_country(country)
    return continent
@geo_api.get('/PolygonByCountry/{country}')
def get_poly_by_country(country:str):
    polygon = geo_helper.get_raw_polygons(country)
    return polygon
@geo_api.get('/CalculateDistance/{country0}/{country1}')
def get_dsistance_between_countries(country0: str, country1: str):
    country0 = geo_helper.get_center_point(country0)
    distance = None
    if country0:
        country1 = geo_helper.get_center_point(country1)
        if country1:
            distance = geo_helper.calculate_distance(country0, country1)
            distance = distance
    return distance if distance else None
@geo_api.get('/CalculateBearing/{country0}/{country1}')
def calculate_bearing(country0: str, country1: str):
    country0 = geo_helper.get_center_point(country0)
    country1 = geo_helper.get_center_point(country1)
    bearing = None
    if country0 and country1:
        bearing = geo_helper.calculate_bearing(country0, country1)
        print(bearing)
    return bearing
@geo_api.get('/ListCountries')
def get_all_countries():
    all_countries = geo_helper.get_all_countries()
    return all_countries
if __name__ == '__main__':
    uvicorn.run('main:geo_api', host='0.0.0.0', port=8000)
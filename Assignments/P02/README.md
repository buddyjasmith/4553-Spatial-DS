# Project: P02
## Buddy Smith
### Description: 
#### The project reads in from the file cities.json. 
####              Load data from the files provided for cities and ufo sightings. We calculate the distance from each city to every other city. Next we average distance to the closest 100 UFO's for each city.
####  

# Files

|  #  | File     | Description                                                                      |
|:---:|----------|----------------------------------------------------------------------------------|
|  1  | Main.py  | Main file that performs all operations                                           |
|  2  | avg_ufo.json | Contains each cities latitude, longitude, and average distance for ufo sightings |
|  3  | distances.json | contains the distance from each city to every other city                         |
|  4  | data/cities.geojson         | contains all pertininent city info                                               |
|  5  | 'data/ufo_data.csv'         | contains relevant ufo sighting info                                              |                              |


# Commands Used
| order | command                    | 
|:------|:---------------------------|
| 1     | brew/apt install pipenv    | 
| 2     | pipenv shell               |
| 3     | pipenv run python3 main.py |
|         
# Modules used
| order | Module     | 
|:------|:-----------|
| 1     | json       | 
| 2     | csv        |
| 3     | pprint     |
| 4     | gopandas   |
| 5     | statistics |
| 6     | shapely    |
| 7     | pydantic   |


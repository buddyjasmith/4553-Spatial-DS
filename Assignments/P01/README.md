# Project: P01
## Buddy Smith
### Description: 
#### The project reads in from the file cities.json. 
####              The data is sorted in mulitple ways to find the largest city 
####              within each state. Then each city is loaded into a geojson 
####              format.  Each city is then linked from west to east via LineStrings

# Files

|  #  | File             | Description                                             |
|:---:|------------------|---------------------------------------------------------|
|  1  | Main.py          | Main driver of my project that launches the program     |
|  2  | cities.json      | JSON file holding all city data                         |
|  3  | EastWest.geojson | final product used to load in openstreetmaps via github |
|  4  | outputfile.json  | json data same as geojson with different extendsion     |
|  4  | pipfile          | pipenv related information|                              |


# Commands Used
| order       | command                    | 
|:------------|:---------------------------|
| 1           | brew install pipenv        | 
| 2           | pipenv shell               | 
| 3           | pipenv install rich        | 
| 3           | pipenv run python3 main.py |
|           


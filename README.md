# omdb-extender
This project extends omdb API.
Main goal is to provide following features:
- get a list of movies from OMDBAPI  based ond provided title and genre,
- loging and registering new users,
- possibility to rate and add reviev of movies,
- adding movies to "Favourite" list,
- adding movies to "To watch" list,
- posspossibility to view rate and reviews of other users.

# Run tips
To run this project install libraries listed in requirements.txt.
After that run following command in ./omdb-extender/omdb_project/ directory:
- python manage.py makemigration
- python manage.py migrate
- python manage.py createcachetable

In settings.py provide your apikey from OMDBAPI in OMDB_API_KEY variable for example:
OMDB_API_KEY = "abc123"
You can obtain your api key from this address: http://www.omdbapi.com/apikey.aspx

To run development server use command:
 - python manage.py runserver
 
 Api should be available from address:
 http://localhost:8000/

# Provided actions:
## Authentication
Get list of users:
  GET /api/user/
 
Create new user:
  POST /api/user/

Get authentication token for user:
  POST /api/user/token
  
To use token add header:
  Authorization: Token my_token
  
## Movies
### OMDBAPI film list
List of movies from omdbapi, you have to specify **title** and can filter by **genre**:
GET /api/movie/?title=your_title&genre=Comedy

### TO-WATCH
Get list of movies to watch of logged in user:
 GET /api/movie/to-watch/

Add movie to list "to watch":
 POST /api/movie/to-watch/

Delete movie from list "to watch":
 DELETE /api/movie/to-watch/<id>

### FAVOURITE
Get list of favourite movies of logged in user:
 GET /api/movie/favourite/

Add movie to list "favourite":
 POST /api/movie/favourite/

Delete movie from list "favourite":
 DELETE /api/movie/favourite/<id>


### REVIEW
Get list of users reviews:
 GET /api/movie/review/

Get list of reviews for particular user:
 GET /api/movie/review/?user=1

Get list of reviews for particular movie:
 GET /api/movie/review/?movie_id=tt12345

Get particular review:
 GET /api/movie/review/<id>
  
Add new review:
 POST /api/movie/review/

Delete review:
 DELETE /api/movie/review/<id>

Update review:
PUT /api/movie/review/<id>
PATCH /api/movie/review/<id>

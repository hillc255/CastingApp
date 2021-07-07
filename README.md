TITLE
Movie-Robots: Casting Application

URL
https://git.heroku.com/cast-app.git


PURPOSE
Movie-Robots casting application models a company that is responsible for documenting movies with robot actors.  Movies and robots can be viewed, added, updated, deleted and searched in the application.  This is the capstone project for Udacity's Full-Stack Web Nanodegree program.


APPLICATION STRUCTURE

Backend
Python==3.7.4
PostgreSQL v.13

Key Backend Dependencies
Flask==1.0.2  
Flask-Cors==3.0.8
SQLAlchemy==1.3.3

Frontend
angular-cli==11.1.4

  
Run application locally

1.Clone application
2.Create a virtual environment (example using Anadonda)
(base) C:\CastingApp>.\env\Scripts\activate

3.Install requirements and freeze them
(env) (base) C:\CastingApp> pip install -r requirements.txt
(env) (base) C:\CastingApp> pip freeze > requirements.txt

4.Add and update code and post to Heroku or github
(env) (base) C:\CastingApp> git add . && git commit -m "Update"
(env) (base) C:\CastingApp> git push heroku main
(env) (base) C:\CastingApp> git push origin main

5.Open a terminal to view heroku logs
C:\CastingApp> heroku logs --tail

6.Open another terminal - compile frontend code
CastingApp>frontends> src $ ng serve --port 8081

7.View frontend - locally automatically reloads with source file changes
http://localhost:8081/movies

8.Locally run unittests
Create PostgreSQL database locally and run the api unittests
C:\CastingApp> python test_app.py

9.Check application is running
https://cast-app.herokuapp.com/


DATABASE (models.py)

Create the database "cast-app" and populate tables - uncomment the following:
app.py.db_drop_and_create_all()


PostgreSQL Database - Heroku CLI

cast-app::DATABASE=> \d
                 List of relations
 Schema |     Name      |   Type   |     Owner
--------+---------------+----------+----------------
 public | actors        | table    | vxcrabcbgadapt
 public | actors_id_seq | sequence | vxcrabcbgadapt
 public | movies        | table    | vxcrabcbgadapt
 public | movies_id_seq | sequence | vxcrabcbgadapt
(4 rows)


cast-app::DATABASE=> \d movies
                                       Table "public.movies"
    Column     |          Type          | Collation | Nullable | Default
---------------+------------------------+-----------+----------+------------------------------------
 id            | integer                |           | not null | nextval('movies_id_seq'::regclass)
 title         | character varying(128) |           | not null |
 release_date  | date                   |           | not null |
 movie_img     | character varying(500) |           | not null |
 movie_publish | boolean                |           | not null |
Indexes:
    "movies_pkey" PRIMARY KEY, btree (id)



cast-app::DATABASE=> \d actors
                                       Table "public.actors"
    Column     |          Type          | Collation | Nullable | Default
---------------+------------------------+-----------+----------+------------------------------------
 id            | integer                |           | not null | nextval('actors_id_seq'::regclass)
 first_name    | character varying(30)  |           | not null |
 last_name     | character varying(30)  |           | not null |
 birth_date    | date                   |           | not null |
 gender        | character varying(10)  |           | not null |
 actor_img     | character varying(500) |           | not null |
 actor_publish | boolean                |           | not null |
Indexes:
    "actors_pkey" PRIMARY KEY, btree (id)



API ENDPOINTS  (app.py)

GET '/api/movies'

    Fetches: All movie titles
    Request Arguments: None
    Returns: A list of movie titles
    Permissions: Public, Director, Assistant can GET and view this endpoint.

GET '/api//movies/id'

    Fetches: A single movie data.
    Request Arguments: id
    Returns: All movie data for a single movie.
    Permissions: Director and Assistant can GET and view this endpoint.

POST '/api/movies'

    Fetches: Movie data representation.
    Request Arguments: Input string with movie data for each movie.
    Returns: Movie array added to list of movies.
    Permissions: Director can POST with this endpoint.

PATCH '/api/movies/id'

    Fetches: Single movie data representation.
    Request Arguments: Unique id - primary key: value of existing movie id.
    Returns: Movie array of single movie.
    Permission: Assistant can PATCH with this endpoint.

PATCH '/api/movies/id/publish' or /api/movies/id/unpublish'

    Fetches: Single movie data representation.
    Request Arguments: Unique id - primary key: value of existing movie id.
    Returns: Movie boolean for publish / unpublish.
    Permission: Assistant can PATCH with this endpoint.

DELETE '/api/movies/id'

    Fetches: Single movie data representation.
    Request Arguments: Unique id - primary key: value of existing movie id.
    Returns: Movie array of the single deleted movie data.
    Permission: Director can DELETE with this endpoint.

SEARCH '/api/movies/search'

    Fetches: Searches for like movie title.
    Request Arguments: Any input.
    Returns: Any title like search query.
    Permission: Public, Director, Assistant can SEARCH with this endpoint.

GET '/api/actors'

    Fetches: All actor titles
    Request Arguments: None
    Returns: A list of actor titles
    Permissions: Public, Director, Assistant can GET and view this endpoint.

GET '/api/actors/id'

    Fetches: A single actor data.
    Request Arguments: id
    Returns: All actor data for a single actor.
    Permissions: Director and Assistant can GET and view this endpoint.

POST '/api/actors'

    Fetches: Actor data representation.
    Request Arguments: Input string with actor data for each actor.
    Returns: Actor array added to list of actors.
    Permissions: Director can POST with this endpoint.

PATCH '/api/actors/id'

    Fetches: Single actor data representation.
    Request Arguments: Unique id - primary key: value of existing actor id.
    Returns: Actor array of single actor.
    Permission: Assistant can PATCH with this endpoint.

PATCH '/api/actors/id/publish' or '/api/actors/id/unpublish'

    Fetches: Single actor data representation.
    Request Arguments: Unique id - primary key: value of existing actor id.
    Returns: Actor boolean for publish / unpublish.
    Permission: Assistant can PATCH with this endpoint.

DELETE '/api/actors/id'

    Fetches: Single actor data representation.
    Request Arguments: Unique id - primary key: value of existing actor id.
    Returns: Actor array of the single deleted actor data.
    Permission: Director can DELETE with this endpoint.

SEARCH '/api/actors/search'

    Fetches: Searches for like actor first name.
    Request Arguments: Any inpuy.
    Returns: Any actor first name like search query.
    Permission: Public, Director, Assistant can SEARCH with this endpoint.


AUTHENTICATION & AUTHORIZATION (auth.py)

Auth0 Universal Login is used for authentication
Auth0 authorizes two roles, Assistant and Director, to access APIs

role: Assistant
login: assistant.cast.app@gmail.com
password: <request assistant password>

role: Director
login: director.cast.app@gmail.com
password: <request director password>

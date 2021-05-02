# Standard library imports
import os
import sys

# Third party imports
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

import json
import simplejson
from simplejson import dumps

from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_moment import Moment

# Local application imports
from backend.src.database.models import db_drop_and_create_all, setup_db, Movie, Actor, MovieActorLink, db
from backend.src.auth.auth import AuthError, requires_auth

print(f"**** app.py ****")

# # Third party imports
# try:

#     from flask import Flask, request, abort, jsonify
#     from flask_sqlalchemy import SQLAlchemy
#     #from sqlalchemy import exc

#     import json
#     import simplejson
#     from simplejson import dumps

#     from flask_cors import CORS, cross_origin
#     from flask_migrate import Migrate
#     from flask_moment import Moment

#     # Local application imports
#     from .database.models import db_drop_and_create_all, setup_db, Movie, Actor, MovieActorLink
#     from backend.src.auth.auth import AuthError, requires_auth


# except Exception as e:
#     print(e)

def create_app(test_config=None):
    app = Flask(__name__)
    moment = Moment(app)
    setup_db(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # create and configure the app
    CORS(app)

    # Added CORS and after_request decorator to set Access-Control-Allow
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Application is running...'
        }), 200


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                         'GET, PATCH, PUT, POST, DELETE, OPTIONS')
        #response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000/')
        return response

    # Test cors is working
    @app.route('/test_cors')
    @cross_origin()
    def get_messages():
        return 'CORS is working...'

    # @app.route('/<path:page>')
    # def fallback(page):
    #     return render_template('index.html')


    # uncomment if want to drop and create database
    #db_drop_and_create_all() 

    # '''
    # MOVIES APIS
    #
    # getAllMovies
    # getMovie
    # createMovie
    # updateMovie
    # deleteMovie
    # deleteAllMovies
    # findMovieByTitle
    #
    # '''

    # '''
    #     GET /movies 
    #         a public endpoint
    #         contains all movies data representation
    #     returns status code 200 and json {"success": True, "movies": movies}
    #     where movies is the list of movies
    #      or appropriate status code indicating reason for failure
    #
    #      curl --request GET http://127.0.0.1:5000/movies
    #
    # '''

    @app.route('/movies', methods=['GET'])
    def getAllMovies():

        movies_all = Movie.query.all()

        if len(movies_all) == 0:
            abort(404)

        try:  
            results = []

            for i, movieObj in enumerate(movies_all):
                results.append(json.loads(movieObj.to_json()))

            return jsonify(results)

        except Exception as e:
            print('\n'+'Error getting movies records: ', e)
            abort(404)
    
    # '''
    #     GET /movies/<int:movie_id>
    #         a public endpoint
    #         contains a single movie data representation
    #     returns status code 200 and json {"success": True, "movie": movie}
    #     where movie is a single movie by id
    #     or appropriate status code indicating reason for failure
    #
    #     curl -X GET http://127.0.0.1:5000/movies/1
    #
    # '''


    @app.route('/movies/<int:id>', methods=['GET'])
    #@requires_auth('get:movies')
    def getMovie(id):

        if id is None:
            abort(404)

        movie_query = Movie.query.get(id)

        if movie_query is None:
            abort(404)

        data = {  
            "id": movie_query.id,
            "title": movie_query.title,
            "release_date": str(movie_query.release_date),
            "movie_img": movie_query.movie_img,
            "movie_publish": movie_query.movie_publish
        }

        try:
            return jsonify({
                'success': True,
                'movie': data
            }), 200

        except Exception as e:
            print('\n'+'Error getting movie detail record: ', e)
            abort(404)

    # '''
    # create movie
    # This endpoint to POST a new movie
    # 
    # curl --header "Content-Type: application/json" --request POST --data "{\"title\":\"Great movie\",\"release_date\":\"2021-03-14\",\"movie_img\":\"https://github.com/hillc255/YelpCamp\",\"movie_publish\": true}" http://127.0.0.1:5000/movies/add 
    # curl --header "Content-Type: application/json" --request POST --data "{\"title\":\"Great movie\",\"release_date\":\"2021-03-14\",\"movie_img\":\"https://github.com/hillc255/YelpCamp\"}" http://127.0.0.1:5000/movies/add
    #
    # '''

    @app.route('/movies', methods=['POST'])
    def createMovie():

        try:
            data = {
                'id': None,
                'title': request.get_json()['title'],
                'release_date': request.get_json()['release_date'],
                'movie_img': request.get_json()['movie_img'],
                'movie_publish': False
            }


            if not ('title' in data and 'release_date' in data \
                and 'movie_img' in data and 'movie_publish' in data):

                abort(422)

            movie = Movie(**data)
            movie.insert()

            return jsonify({
                'success': True
            }), 200

        except Exception as e:
            print('\n'+'Error adding movie record: ', e)
            abort(422)
    
    # '''
    #     PATCH /movies/<int:movie_id>
    #         a public endpoint
    #         contains a single movie data representation to be updated
    #         where <id> is the existing model id
    #         it should respond with a 404 error if <id> is not found
    #         it should update the corresponding row for <id>
    #         it should require the 'patch:movies' permission
    #     returns status code 200 and json {"success": True, "movie": movie}
    #     where movie is a single movie by id
    #     or appropriate status code indicating reason for failure
    #
    # curl --header "Content-Type: application/json" --request PUT --data "{\"title\":\"New movie2\",\"release_date\":\"2021-03-14\",\"movie_img\":\"https://github.com/hillc255/YelpCamp\",\"movie_publish\": true}" http://127.0.0.1:5000/movies/7
    #
    # '''

    @app.route('/movies/<int:id>', methods=['PATCH'])
    #@requires_auth('patch:movies')
    def updateMovie(id):

        if id is None:
            abort(404)

        data = Movie.query.get(id)

        if data is None:
            abort(404)

        request_json = request.get_json()
        data.title = request.json.get('title')
        data.release_date = request.json.get('release_date')
        data.movie_img = request.json.get('movie_img')

        data.update()

        return jsonify({
            "success": True
        }), 200


    @app.route('/movies/<int:id>/publish', methods=['PATCH'])
    #@requires_auth('patch:movies')
    def publishMovie(id):

        if id is None:
            abort(404)

        data = Movie.query.get(id)

        if data is None:
            abort(404)
            
        data.movie_publish = True

        data.update()

        return jsonify({
            "success": True
        }), 200


    @app.route('/movies/<int:id>/unpublish', methods=['PATCH'])
    #@requires_auth('patch:movies')
    def unpublishMovie(id):

        if id is None:
            abort(404)

        data = Movie.query.get(id)

        if data is None:
            abort(404)
            
        data.movie_publish = False

        data.update()

        return jsonify({
            "success": True
        }), 200

    # '''
    # Delete movie
    # Create an endpoint to DELETE question using a question ID.
    # TEST: When you click the trash icon next to a question, the question
    #  will be removed.  This removal will persist in the database and when
    # you refresh the page.
    #
    # curl -X DELETE http://127.0.0.1:5000/movies/6   
    # '''

    @app.route('/movie/<int:id>', methods=['DELETE'])
    def deleteMovie(id):

        try:
            #data = Movie.query.filter(Movie.id == id).one_or_none()
            #data = Movie.query.filter_by(id).delete()
            data = Movie.query.filter_by(id).one_or_none()

            if data is None:
                abort(404)

            data.delete()

            #current_movies = Movie.query.order_by(Movie.title).all()
            # current_movie = paginate_movies(request, selection)

            # return jsonify({
            #     'success': True,
            #     'deleted': id,
            #     'movies': current_movies,
            #     'total_movies': len(Movie.query.all())
            # }), 200

            return jsonify({
                'success': True
            }), 200

        except Exception as e:
            print('\n'+'Error deleting movie record: ', e)
            abort(404)  
 

    # '''
    # GET /movies/title
    #
    # Search /movies?title=[title]
    #
    # curl -X GET http://127.0.0.1:5000/movies/title  
    # '''
    
    @app.route('/movies/search', methods=['GET'])
    def findMovieByTitle():

        search_title = request.args.get('title')

        
        data = Movie.query.filter(
            Movie.title.ilike(f'%{search_title}%')).all()

        if len(data) == 2:
            abort(404)
  
        results = []
        
        try:

            for i, movieObj in enumerate(data):
                results.append(json.loads(movieObj.to_json()))

            return jsonify(results)

        except Exception as e:
            print('\n'+'Error getting movie titles: ', e)
            abort(404) 
   
 
    # '''
    # GET: /actors
    # Authorized:
    # Endpoint: gets all actors data representation
    # Returns status code 200 and json {"success": True, "actors": actors}
    #   where actors is the list of actors
    #   or appropriate status code indicating reason for failure
    # '''

    @app.route('/actors', methods=['GET'])
    def getAllActors():

        actors_all = Actor.query.all()

        if len(actors_all) == 0:
            abort(404)

        try:  
            results = []

            for i, actorObj in enumerate(actors_all):
                results.append(json.loads(actorObj.to_json()))

            return jsonify(results)

        except Exception as e:
            print('\n'+'Error getting actors record: ', e)
            abort(404)


    # '''
    # GET: /actors/<int:id>
    # Authorized:
    # Endpoint:  GET a specific actor
    # Returns: status code 200 and json {"success": True, "actor": data}
    #   where actor is a single actor data
    #   or appropriate status code indicating reason for failure
    # '''

    @app.route('/actors/<int:id>', methods=['GET'])
    #@requires_auth('get:actors')
    def getActor(id):

        if id is None:
            abort(404)

        actor_query = Actor.query.get(id)

        if actor_query is None:
            abort(404)

        data = {
            "id": actor_query.id,
            "first_name": actor_query.first_name,
            "last_name": actor_query.last_name,
            "birth_date": str(actor_query.birth_date),
            "gender": actor_query.gender,
            "actor_img": actor_query.actor_img,
            "actor_publish": actor_query.actor_publish
        }

        try:
            return jsonify({
                'success': True,
                'actor': data
            }), 200

        except Exception as e:
            print('\n'+'Error getting actor detail record: ', e)
            abort(404)
        

    # '''
    # POST: /actors
    # Authorized:
    # Endpoint: create a new actor
    # Returns: status code 200 and json {"success": True}
    #   where actor is a single new actor
    #   or appropriate status code indicating reason for failure
    # '''

    @app.route('/actors', methods=['POST'])
    def createActor():

        try:

            data = {
                'id': None,
                'first_name': request.get_json()['first_name'],
                'last_name': request.get_json()['last_name'],
                'birth_date': request.get_json()['birth_date'],
                'gender': request.get_json()['gender'],
                'actor_img': request.get_json()['actor_img'],
                'actor_publish': request.get_json()['actor_publish']
            }

            if not ('first_name' in data and 'last_name' in data \
                     and 'birth_date' in data and 'gender' in data \
                     and 'actor_img' in data and 'actor_publish' in data):

                    abort(422)

            actor = Actor(**data)
            actor.insert()

            return jsonify({
                'success': True
            }), 200

        except Exception as e:
            print('\n'+'Error adding actor record: ', e)
            abort(422)

 
    # '''
    # PATCH: /actors/<int:id>
    # Authorized:
    # Endpoint:  update actor data fields
    # Returns: status code 200 and json {"success": True}
    #   where actor published is a single actor
    #   or appropriate status code indicating reason for failure
    # '''


    @app.route('/actors/<int:id>', methods=['PATCH'])
    #@requires_auth('patch:actors')
    def updateActor(id):

        if id is None:
            abort(404)

        data = Actor.query.get(id)

        if data is None:
            abort(404)

        request_json = request.get_json()
        data.first_name = request.json.get('first_name')
        data.last_name = request.json.get('last_name')
        data.birth_date = request.json.get('birth_date')
        data.gender = request.json.get('gender')
        data.actor_img = request.json.get('actor_img')
        data.actor_publish = request.json.get('actor_publish')

        data.update()

        return jsonify({
            "success": True
        }), 200

    # '''
    # PATCH: /actors/<int:id>/publish
    # Authorized:
    # Endpoint: publish actor data fields
    # Returns: status code 200 and json {"success": True}
    #   where actor updated is a single actor
    #   or appropriate status code indicating reason for failure
    # '''
    
    @app.route('/actors/<int:id>/publish', methods=['PATCH'])
    #@requires_auth('patch:movies')
    def publishActor(id):

        if id is None:
            abort(404)

        data = Actor.query.get(id)

        if data is None:
            abort(404)
            
        data.actor_publish = True

        data.update()

        return jsonify({
            "success": True
        }), 200


    # '''
    # PATCH: /actors/<int:id>/unpublish
    # Authorized:
    # Endpoint:  unpublish actor data fields
    # Returns: status code 200 and json {"success": True}
    #   where actor unpublish is a single actor
    #   or appropriate status code indicating reason for failure
    # '''


    @app.route('/actors/<int:id>/unpublish', methods=['PATCH'])
    #@requires_auth('patch:actors')
    def unpublishActor(id):

        if id is None:
            abort(404)

        data = Actor.query.get(id)

        if data is None:
            abort(404)
            
        data.actor_publish = False

        data.update()

        return jsonify({
            "success": True
        }), 200


    # '''
    # DELETE: /actors/<int:id>
    # Authorized:
    # Endpoint: Deletes specific actor data fields
    # Returns: status code 200 and json {"success": True}
    #   where actor deleted is a single actor
    #   or appropriate status code indicating reason for failure
    # '''

    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True
            }), 200

        except Exception as e:
            print('\n'+'Error deleting actor record: ', e)
            abort(404)


    # '''
    # SEARCH: /actors/search
    # Authorized:
    # Endpoint: Provide a like search for actor first-name
    # Returns: status code 200 and json {"success": True}
    #   where actor(s) are searched for by first-name
    #   or appropriate status code indicating reason for failure
    # '''
    
    @app.route('/actors/search', methods=['GET'])
    def findActorByFirstName():

        search_firstname = request.args.get('first_name')
        
        data = Actor.query.filter(
            Actor.first_name.ilike(f'%{search_firstname}%')).all()

        if len(data) == 2:
            abort(404)
  
        results = []
        
        try:

            for i, actorObj in enumerate(data):
                results.append(json.loads(actorObj.to_json()))

            return jsonify(results)

        except Exception as e:
            print('\n'+'Error getting actor first name: ', e)
            abort(404) 



    # MANY TO MANY RELATIONSHIP add actor to movie
    # @app.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=['POST'])
    # def addActorToMovie(movie_id, actor_id)

    # MANY TO MANY RELATIONSHIP remove actor from movie
    # @app.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=['Delete'])
    # def removeActorToMovie(movie_id, actor_id)

    # MANY TO MANY RELATIONSHIP add movie to an actor
    # @app.route('/actors/<int:actor_id>/movies/<int:movie_id>', methods=['POST'])
    # def addMovieToActor(actor_id, movie_id)

    # MANY TO MANY RELATIONSHIP remove movie from an actor
    # @app.route('/actors/<int:actor_id>/movies/<int:movie_id>', methods=['DELETE'])
    # def removeMovieToActor(actor_id, movie_id)

    # MANY TO MANY RELATIONSHIP Get all Actors for a movie
    # @app.route('/movies/<int:movie_id>/actors', methods=['GET'])
    # def get_all_actors_for_movie(id):

    # MANY TO MANY RELATIONSHIP Get all Movies for the actor with id=id
    # @app.route('/actors/<int:actor_id>/movies', methods=['GET'])
    # def get_all_movies_for_actor(actor_id):
    #     try:

    #         if id is None:
    #             abort(404)

    #         actor = Actor.query.get(id)

    #         if actor is None:
    #             abort(404)

    #         #return jsonify(Actor.movies.any(id=actor.id)), 200
    #         return jsonify(actor.movies.query.all()), 200

    #     except Exception as e:
    #         print('\n'+'Error fetching movies for actor record: ', e)
    #         abort(404)


    '''
    Error handlers for all expected errors including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
         }), 405

    return app

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run()
    # port = int(os.environ.get("PORT",5000))
    # app.run(host='127.0.0.1',port=port,debug=True)

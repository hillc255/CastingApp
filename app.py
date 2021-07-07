# Standard library imports
import os
import sys

# Third party imports
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

import json
import simplejson
from simplejson import dumps

from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_moment import Moment

# Local application imports
from backend.src.database.models import db_drop_and_create_all, \
    setup_db, Movie, Actor, db
from backend.src.auth.auth import AuthError, requires_auth, requires_role

print(f"**** app.py ****")


def create_app(test_config=None):
    app = Flask(__name__)
    moment = Moment(app)
    setup_db(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # Create and configure the app
    CORS(app)

    # Added CORS and after_request decorator to set Access-Control-Allow
    CORS(app, resources={r"/*": {
        "origins": "*"
    }})

    # Serve the Angular app
    @app.route('/actors', defaults={'u_path': ''})
    @app.route('/', defaults={'u_path': ''})
    @app.route('/movies', defaults={'u_path': ''})
    @app.route('/movies/<path:u_path>')
    @app.route('/actors/<path:u_path>')
    def index(u_path):
        return render_template('index.html')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST, DELETE, OPTIONS')
        return response

    # Test cors is working
    @app.route('/test_cors')
    @cross_origin()
    def get_messages():
        return 'CORS is working...'

    # Uncomment if want to drop and create database
    # db_drop_and_create_all()

    # '''
    # MOVIE APIs
    #
    # '''

    # '''
    # GET:          /api/movies
    # Authorized:   Public user access
    # Endpoint:     Gets all movies data representation
    # Returns:      Status code 200 for successful get
    #               where movies is the list of movies
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/movies', methods=['GET'])
    def getAllMovies():

        movies_all = Movie.query.order_by(Movie.title).all()

        if len(movies_all) == 0:
            abort(404)

        try:
            results = []

            for i, movieObj in enumerate(movies_all):
                results.append(json.loads(movieObj.to_json()))

            return jsonify(results), 200

        except Exception as e:
            print('\n'+'Error getting all movie records: ', e)
            abort(404)

    # '''
    # GET:          /api/movies/<int:id>
    # Authorized:   Director or Assistant access
    # Endpoint:     GET2 a specific movie
    # Returns:      Status code 200 and json {"success": True, "movie": data}
    #               where movie is a single movie data
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/movies/<int:id>', methods=['GET'])
    @requires_role(['director', 'assistant'])
    def getMovie(id):

        if id is None:
            abort(404)

        movie_query = Movie.query.filter(Movie.id == id).one_or_none()

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
    # POST:         /api/movies
    # Authorized:   Director access
    # Endpoint:     Create a new movie
    # Returns:      Status code 200 and json {"success": True}
    #               where movie is a single new movie
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/movies', methods=['POST'])
    @requires_role('director')
    def createMovie():

        try:
            data = {
                'id': None,
                'title': request.get_json()['title'],
                'release_date': request.get_json()['release_date'],
                'movie_img': request.get_json()['movie_img'],
                'movie_publish': False
            }

            if not ('title' in data and 'release_date' in data
                    and 'movie_img' in data and 'movie_publish' in data):

                abort(422)

            movie = Movie(**data)
            movie.insert()

            return jsonify({
                'success': True
            }), 200

        except Exception as e:
            print('\n'+'Error creating movie record: ', e)
            abort(422)

    # '''
    # PATCH:        /api/movies/<int:id>
    # Authorized:   Assistant access
    # Endpoint:     Update movie data fields
    # Returns:      Status code 200 and json {"success": True}
    #               where movie published is a single movie
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/movies/<int:id>', methods=['PATCH'])
    @requires_role('assistant')
    def updateMovie(id):

        if id is None:
            abort(404)

        data = Movie.query.filter(Movie.id == id).one_or_none()

        if data is None:
            abort(404)

        request_json = request.get_json()
        data.title = request.json.get('title')
        data.release_date = request.json.get('release_date')
        data.movie_img = request.json.get('movie_img')

        try:
            data.update()

            return jsonify({
                "success": True
             }), 200

        except Exception as e:
            print('\n'+'Error updating movie record: ', e)
            abort(422)

    # '''
    # PATCH:        /api/movies/<int:id>/publish
    # Authorized:   Assistant access
    # Endpoint:     Publish movie data fields - boolen
    # Returns:      Status code 200 and json {"success": True}
    #               where movie updated is a single movie
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/movies/<int:id>/publish', methods=['PATCH'])
    @requires_role('assistant')
    def publishMovie(id):

        if id is None:
            abort(404)

        data = Movie.query.filter(Movie.id == id).one_or_none()

        if data is None:
            abort(404)

        data.movie_publish = True

        try:
            data.update()

            return jsonify({
                "success": True
            }), 200

        except Exception as e:
            print('\n'+'Error publishing movie record: ', e)
            abort(422)

    # '''
    # PATCH:        /api/movies/<int:id>/publish
    # Authorized:   Assistant access
    # Endpoint:     Unpublish movie data fields - boolen
    # Returns:      Status code 200 and json {"success": True}
    #               where movie updated is a single movie
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/movies/<int:id>/unpublish', methods=['PATCH'])
    @requires_role('assistant')
    def unpublishMovie(id):

        if id is None:
            abort(404)

        data = Movie.query.filter(Movie.id == id).one_or_none()

        if data is None:
            abort(404)

        data.movie_publish = False

        try:
            data.update()

            return jsonify({
                "success": True
            }), 200

        except Exception as e:
            print('\n'+'Error unpublishing movie record: ', e)
            abort(422)

    # '''
    # DELETE:       /api/movies/<int:id>
    # Authorized:   Director access
    # Endpoint:     Deletes specific movie data fields
    # Returns:      Status code 200 and json {"success": True}
    #               where movie deleted is a single movie
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/movies/<int:id>', methods=['DELETE'])
    @requires_role('director')
    def deleteMovie(id):

        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True
            }), 200

        except Exception as e:
            print('\n'+'Error deleting movie record: ', e)
            abort(404)

    # '''
    # SEARCH:       /api/movies/search
    # Authorized:   Public user access
    # Endpoint:     Provide a like search for movie title
    # Returns:      Status code 200 if search is successful
    #               where movie(s) are searched for by title
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/movies/search', methods=['GET'])
    def findMovieByTitle():

        search_title = request.args.get('title')

        data = Movie.query.filter(
            Movie.title.ilike(f'%{search_title}%')).all()

        results = []

        try:
            for i, movieObj in enumerate(data):
                results.append(json.loads(movieObj.to_json()))

            return jsonify(results), 200

        except Exception as e:
            print('\n'+'Error searching by movie titles: ', e)
            abort(404)

    # '''
    # ACTOR ENDPOINTS
    #
    # '''

    # '''
    # GET:          /api/actors
    # Authorized:   Public user access
    # Endpoint:     Gets all actors data representation
    # Returns:      Status code 200 for successful get
    #               where actors is the list of actors
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/actors', methods=['GET'])
    def getAllActors():

        actors_all = Actor.query.order_by(Actor.first_name).all()

        if len(actors_all) == 0:
            abort(404)

        try:
            results = []

            for i, actorObj in enumerate(actors_all):
                results.append(json.loads(actorObj.to_json()))

            return jsonify(results), 200

        except Exception as e:
            print('\n'+'Error getting all actor records: ', e)
            abort(404)

    # '''
    # GET:          /api/actors/<int:id>
    # Authorized:   Director or Assistant access
    # Endpoint:     GET a specific actor
    # Returns:      Status code 200 and json {"success": True, "actor": data}
    #               where actor is a single actor data
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/actors/<int:id>', methods=['GET'])
    @requires_role(['director', 'assistant'])
    def getActor(id):

        if id is None:
            abort(404)

        actor_query = Actor.query.filter(Actor.id == id).one_or_none()

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
    # POST:         /api/actors
    # Authorized:   Director access
    # Endpoint:     Create a new actor
    # Returns:      Status code 200 and json {"success": True}
    #               where actor is a single new actor
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/actors', methods=['POST'])
    @requires_role('director')
    def createActor():

        try:

            data = {
                'id': None,
                'first_name': request.get_json()['first_name'],
                'last_name': request.get_json()['last_name'],
                'birth_date': request.get_json()['birth_date'],
                'gender': request.get_json()['gender'],
                'actor_img': request.get_json()['actor_img'],
                'actor_publish': False
            }

            if not ('first_name' in data and 'last_name' in data
                    and 'birth_date' in data and 'gender' in data
                    and 'actor_img' in data and 'actor_publish' in data):

                abort(422)

            actor = Actor(**data)
            actor.insert()

            return jsonify({
                'success': True
            }), 200

        except Exception as e:
            print('\n'+'Error creating actor record: ', e)
            abort(422)

    # '''
    # PATCH:        /api/actors/<int:id>
    # Authorized:   Assistant access
    # Endpoint:     Update actor data fields
    # Returns:      Status code 200 and json {"success": True}
    #               where actor published is a single actor
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/actors/<int:id>', methods=['PATCH'])
    @requires_role('assistant')
    def updateActor(id):

        if id is None:
            abort(404)

        data = Actor.query.filter(Actor.id == id).one_or_none()

        if data is None:
            abort(404)

        request_json = request.get_json()
        data.first_name = request.json.get('first_name')
        data.last_name = request.json.get('last_name')
        data.birth_date = request.json.get('birth_date')
        data.gender = request.json.get('gender')
        data.actor_img = request.json.get('actor_img')

        try:
            data.update()

            return jsonify({
                "success": True
            }), 200

        except Exception as e:
            print('\n'+'Error updating actor record: ', e)
            abort(422)

    # '''
    # PATCH:        /api/actors/<int:id>/publish
    # Authorized:   Assistant access
    # Endpoint:     Publish actor data fields - boolen
    # Returns:      Status code 200 and json {"success": True}
    #               where actor updated is a single actor
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/actors/<int:id>/publish', methods=['PATCH'])
    @requires_role('assistant')
    def publishActor(id):

        if id is None:
            abort(404)

        data = Actor.query.filter(Actor.id == id).one_or_none()

        if data is None:
            abort(404)

        data.actor_publish = True

        try:
            data.update()

            return jsonify({
                "success": True
            }), 200

        except Exception as e:
            print('\n'+'Error publishing actor record: ', e)
            abort(422)

    # '''
    # PATCH:        /api/actors/<int:id>/unpublish
    # Authorized:   Assistant access
    # Endpoint:     Unpublish actor data fields - boolean
    # Returns:      Status code 200 and json {"success": True}
    #               where actor unpublish is a single actor
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/actors/<int:id>/unpublish', methods=['PATCH'])
    @requires_role('assistant')
    def unpublishActor(id):

        if id is None:
            abort(404)

        data = Actor.query.filter(Actor.id == id).one_or_none()

        if data is None:
            abort(404)

        data.actor_publish = False

        try:
            data.update()

            return jsonify({
                "success": True
            }), 200

        except Exception as e:
            print('\n'+'Error unpublishing actor record: ', e)
            abort(422)

    # '''
    # DELETE:       /api/actors/<int:id>
    # Authorized:   Director access
    # Endpoint:     Deletes specific actor data fields
    # Returns:      Status code 200 and json {"success": True}
    #               where actor deleted is a single actor
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/actors/<int:id>', methods=['DELETE'])
    @requires_role('director')
    def deleteActor(id):
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
    # SEARCH:       /api/actors/search
    # Authorized:   Public user access
    # Endpoint:     Provide a like search for actor first-name
    # Returns:      Status code 200 if search is successful
    #               where actor(s) are searched for by first-name
    #               or appropriate status code indicating reason for failure
    # '''

    @app.route('/api/actors/search', methods=['GET'])
    def findActorByFirstName():

        search_firstname = request.args.get('first_name')

        data = Actor.query.filter(
            Actor.first_name.ilike(f'%{search_firstname}%')).all()

        results = []

        try:

            for i, actorObj in enumerate(data):
                results.append(json.loads(actorObj.to_json()))

            return jsonify(results), 200

        except Exception as e:
            print('\n'+'Error searching by actor first name: ', e)
            abort(404)

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

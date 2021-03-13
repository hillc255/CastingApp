import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_moment import Moment

from .database.models import db_drop_and_create_all, setup_db, Movie, Actor, MovieActorLink
from .auth.auth import AuthError, requires_auth

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

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                         'GET, PATCH, PUT, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # uncomment if want to drop and create database
    #db_drop_and_create_all() 

    @app.route('/')
    def hello():
        return jsonify({
            'success': True,
            'message': 'Home page'
        }), 200

    return app

app = create_app()

# '''
#     GET /actors
#     public endpoint
#     contains all actors data representation
#     returns status code 200 and json {"success": True, "actors": actors}
#     where actors is the list of actors
#         or appropriate status code indicating reason for failure
# '''

@app.route('/actors', methods=['GET'])
def get_actors():

    actors = Actor.query.all()

    for actor in actors:

    if len(actors) == 0:
        abort(404)

    try:
        return jsonify({
            'success': True,
            'actors': actors
        }), 200

    except Exception as e:
        print('\n'+'Error getting actors record: ', e)
        abort(404)


# '''
#     GET /movies
#         it should be a public endpoint
#         it should contain all actors data representation
#     returns status code 200 and json {"success": True, "actors": actors}
#      where actors is the list of actors
#         or appropriate status code indicating reason for failure
# '''

# @app.route('/movies', methods=['GET'])
# def get_movies():

#     movies = Movie.query.all()

#     if len(movies) == 0:
#         abort(404)

#     try:
#         return jsonify({
#             'success': True,
#             'movies': movies
#         }), 200

#     except Exception as e:
#         print('\n'+'Error getting movies record: ', e)
#         abort(404)


# '''
# add actors

# Create an endpoint to POST a new question,
# which will require the question and answer text,
# category, and difficulty score.
# TEST: When you submit a question on the "Add" tab,
# the form will clear and the question will appear at the end
# of the last page of the questions list in the "List" tab.

# '''

# @app.route('/actors/add', methods=['POST'])
# def add_actor():

#     try:
#         data = {
#             'first_name': request.get_json()['first_name'],
#             'last_name': request.get_json()['last_name'],
#             'birth_date': request.get_json()['birth_date'],
#             'gender': request.get_json()['gender']
#          }

#         if not ('first_name' in data and 'last_name' in data and
#                 'birth_date' in data and 'gender' in data
#                 ):
#                 abort(422)

#             # data_category = int(data['category'])
#             # data_difficulty = int(data['difficulty'])

#             # if not (1 <= data_category <= 6) and (1 <= data_difficulty <= 4):
#             #     abort(422)

#         actor = Actor(**data)
#         actor.insert()

#         return jsonify({
#             'success': True
#         }), 200

#     except Exception as e:
#         print('\n'+'Error adding actor record: ', e)
#         abort(422)



# '''
# add movie

# Create an endpoint to POST a new question,
# which will require the question and answer text,
# category, and difficulty score.
# TEST: When you submit a question on the "Add" tab,
# the form will clear and the question will appear at the end
# of the last page of the questions list in the "List" tab.

# '''
# @app.route('/movies/add', methods=['POST'])
# def add_movie():

#     try:
#         data = {
#               'title': request.get_json()['title'],
#               'release_date': request.get_json()['release_date']
#         }

#         if not ('title' in data and 'release_date' in data):
#             abort(422)

#             # data_category = int(data['category'])
#             # data_difficulty = int(data['difficulty'])

#             # if not (1 <= data_category <= 6) and (1 <= data_difficulty <= 4):
#             #     abort(422)

#         movie = Movie(**data)
#         movie.insert()

#         return jsonify({
#             'success': True
#         }), 200

#     except Exception as e:
#         print('\n'+'Error adding movie record: ', e)
#         abort(422)


# '''
# update actor

#  Implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where
#         drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
#         --Note: changed return array from drink to drinks as the array
# '''

# @app.route('/actors/<int:actor_id>', methods=['PATCH'])
# #@requires_auth('patch:actors')
# def update_actor(payload, actor_id):

#     if actor_id is None:
#         abort(404)

#     actor = Actor.query.get(actor_id)

#     if actor is None:
#         abort(404)

#     request_json = request.get_json()
#     actor.first_name = request.json.get('first_name')
#     actor.last_name = request.json.get('last_name')
#     actor.birth_date = request.json.get('birth_date')
#     actor.gender = request.json.get('gendre')
#     #actor.last_name = json.dumps(request_json.get('recipe'))

#     actor.update()
#     # actors = []
#     # actors.append(drink.long())

#     return jsonify({
#         "success": True,
#         "drinks": actors
#         }), 200



# '''
#  @TODO - Done:
#  Implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where
#         drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
#         --Note: changed return array from drink to drinks as the array
# '''


# @app.route('/movies/<int:movie_id>', methods=['PATCH'])
# #@requires_auth('patch:movies')
# def update_movie(payload, movie_id):

#     if movie_id is None:
#         abort(404)

#     movie = Movie.query.get(movie_id)

#     if movie is None:
#         abort(404)

#     request_json = request.get_json()
#     movie.title = request.json.get('title')
#     movie.release_date = request.json.get('release_date')

#     movie.update()
#     # movies = []
#     # drinks.append(drink.long())

#     return jsonify({
#         "success": True,
#         "movies": movies
#         }), 200


# '''

# '''
# Delete actors

# Create an endpoint to DELETE question using a question ID.
# TEST: When you click the trash icon next to a question, the question
# will be removed.  This removal will persist in the database and when
# you refresh the page.
# '''
# @app.route('/actors/<int:id>', methods=['DELETE'])
# def delete_actor(id):
#     try:
#         actor = Actor.query.filter(Actor.id == id).one_or_none()

#         if actor is None:
#             abort(404)

#         actor.delete()

#         selection = Actor.query.order_by(Actor.id).all()
#         current_actors = paginate_actors(request, selection)

#         return jsonify({
#             'success': True,
#             'deleted': id,
#             'actor': actor,
#             'total_actors': len(Actor.query.all())
#         }), 200

#     except Exception as e:
#         print('\n'+'Error deleting actor record: ', e)
#         abort(404)

# '''
# Delete movie
# Create an endpoint to DELETE question using a question ID.
# TEST: When you click the trash icon next to a question, the question
#  will be removed.  This removal will persist in the database and when
# you refresh the page.
# '''
# @app.route('/movie/<int:id>', methods=['DELETE'])
# def delete_movie(id):
#     try:
#         movie = Movie.query.filter(Movie.id == id).one_or_none()

#         if movie is None:
#             abort(404)

#         movie.delete()
#         selection = Movie.query.order_by(Movie.id).all()
#         current_movie = paginate_movies(request, selection)

#         return jsonify({
#             'success': True,
#             'deleted': id,
#             'movies': current_movies,
#             'total_movies': len(Movie.query.all())
#         }), 200

#     except Exception as e:
#         print('\n'+'Error deleting movie record: ', e)
#         abort(404)

# '''
# @TODO - Done
# Create error handlers for all expected errors including 404 and 422.
# '''
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "success": False,
#         "error": 404,
#         "message": "Resource Not Found"
#     }), 404

# @app.errorhandler(422)
# def unprocessable(error):
#     return jsonify({
#         "success": False,
#         "error": 422,
#         "message": "Unprocessable"
#     }), 422

# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify({
#         "success": False,
#         "error": 400,
#         "message": "Bad Request"
#      }), 400

# @app.errorhandler(405)
# def not_allowed(error):
#     return jsonify({
#         "success": False,
#         "error": 405,
#         "message": "Method Not Allowed"
#     }), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run()

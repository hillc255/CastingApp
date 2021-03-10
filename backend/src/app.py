import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
#from flask_migrate import Migrate
#from flask_moment import Moment

#from database.models import setup_db, Dbmovie, Movie, Actor
from database import models

def create_app(test_config=None):
    app = Flask(__name__)
    #moment = Moment(app)
    # models.setup_db(app)
    db = SQLAlchemy(app)
    # migrate = Migrate(app, db)
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

    #set envrionmental variable
    #os.environ['EXCITED'] = 'true' 

    @app.route('/')
    def hello():
        return jsonify({
            'success': True,
            'message': 'Home page'
        }), 200

    # def get_greeting():
    #     excited = os.getenv('EXCITED')
    #     greeting = "Hello" 
    #     if excited == 'true': greeting = greeting + "!!!!!"
    #     return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run()

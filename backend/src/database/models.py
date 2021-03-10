import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer, Date, ForeignKey, create_engine
#from app import db
from flask_sqlalchemy.model import DefaultMeta
# from flask_migrate import Migrate
# from sqlalchemy.ext.declarative import DeclarativeMeta

db = SQLAlchemy()

BaseModel: DefaultMeta = db.Model

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'picasso0')
DB_NAME = os.getenv('DB_NAME', 'castapp')
database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

# migrate = Migrate(app, db)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

#def setup_db(app, database_path=database_path):
def setup_db(app): 
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Casting Agency Specifications
The Casting Agency models a company that is responsible for creating 
movies and managing and assigning actors to those movies. 
You are an Executive Producer within the company and are creating a 
system to simplify and streamline your process.

Models:
Movies with attributes title and release date
Actors with attributes name, age and gender
'''
class Dbmovie(BaseModel):
    __tablename__ = 'dbmovies'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, ForeignKey('movies.id'))
    actor_id = db.Column(db.Integer, ForeignKey('actors.id'))
    movie = relationship("Actor", backref=backref("dbmovies", cascade="all, delete-orphan"))
    actor = relationship("Movie", backref=backref("dbmovies", cascade="all, delete-orphan"))

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    release_date = db.Column(db.DATE, nullable=False) 
    actors = relationship("Actor", secondary="movies")


    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
           'id': self.id,
           'title': self.title,
           'release_date': self.release_date
        }

class Actor(db.Model):  
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    movies = relationship("Movie", secondary="actors")

    def __init__(self, first_name, last_name, birth_date, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender

    def format(self):
        return {
          'id': self.id,
          'first_name': self.first_name,
          'last_name': self.last_name,
          'birth_date': self.birth_date,
          'gender': self.gender}



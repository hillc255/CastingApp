import os
import sys

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer, Date, ForeignKey, create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
import json
import simplejson
from simplejson import dumps

print(f"*********************************BEFORE SQLALHENY")

db = SQLAlchemy()

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'picasso0')
DB_NAME = os.getenv('DB_NAME', 'castapp')
DB_URL = os.getenv('DB_URL', 'castapp')

print(f"1) DB_HOST={DB_HOST}")
print(f"2) DB_USER={DB_USER}")
print(f"3) DB_PASSWORD={DB_PASSWORD}")
print(f"4) DB_NAME={DB_NAME}")
print(f"5) DB_URL={DB_URL}")

database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

print(f"*********************************database_path={database_path}")

# create database
engine = create_engine(database_path)

print(f"********************************engine={engine}")

#engine = create_engine(DB_URL)
if database_exists(engine.url):
    pass
    #drop_database(engine.url)
    #sys.exit("Drop database - exit")
    #create_database(engine.url)

#if not database_exists(engine.url):
else:
    create_database(engine.url)

print(f"TEST ******* AFTER db exists={database_exists(engine.url)}")

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
    !!NOTE you can change the database_filename variable to have multiple versions of a database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db.session.execute("ALTER SEQUENCE movies_id_seq RESTART WITH 1")
    db.session.execute("ALTER SEQUENCE actors_id_seq RESTART WITH 1")
    db.session.add_all([movie1, movie2, movie3, movie4, movie5, movie6]) 
    db.session.add_all([actor1, actor2, actor3, actor4, actor5, actor6, actor7]) 
    db.session.commit()
    db.session.add_all([movieactor1, movieactor2, movieactor3, movieactor4, movieactor5, movieactor6, movieactor7, movieactor8, movieactor9]) 
    db.session.commit()

'''
Models

Casting Agency Specifications
The Casting Agency models a company that is responsible for creating 
movies and managing and assigning actors to those movies. 
You are an Executive Producer within the company and are creating a 
system to simplify and streamline your process.
'''
'''
Association table for movies and actors table
Movies with attributes title and release date
Actors with attributes name, age and gender
'''

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    release_date = db.Column(db.Date, nullable=False) 
    movie_img = db.Column(db.String(500), nullable=False)
    movie_publish = db.Column(db.Boolean, nullable=False)
    actors = relationship('Actor', secondary='movie_actor_link')

    def __init__(self, id, title, release_date, movie_img, movie_publish):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.movie_img = movie_img
        self.movie_publish = movie_publish

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
           'release_date': self.release_date,
           'movie_img': self.movie_img,
           'movie_publish': self.movie_publish
        }
    
    def to_json(self):
        json_movie = dumps({
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y%m%d"),
            'movie_img': self.movie_img,
            'movie_publish': self.movie_publish
        })
        return json_movie

class Actor(db.Model):  
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    actor_img = db.Column(db.String(500), nullable=False)
    actor_publish = db.Column(db.Boolean, nullable=False)
    movies = relationship('Movie', secondary='movie_actor_link')

    def __init__(self, id, first_name, last_name, birth_date, gender, actor_img, actor_publish):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.actor_img = actor_img
        self.actor_publish = actor_publish

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
          'first_name': self.first_name,
          'last_name': self.last_name,
          'birth_date': self.birth_date,
          'gender': self.gender,
          'actor_img': self.actor_img,
          'actor_publish': self.actor_publish
        }

    def to_json(self):
        json_actor = dumps({
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.strftime("%Y%m%d"),
            'gender': self.gender,
            'actor_img': self.actor_img,
            'actor_publish': self.actor_publish
        })
        return json_actor


class MovieActorLink(db.Model):
    __tablename__ = 'movie_actor_link'

    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.id'), primary_key=True)
    movie = relationship('Actor', backref=backref('movie_actor_link', cascade='all, delete-orphan'))
    actor = relationship('Movie', backref=backref('movie_actor_link', cascade='all, delete-orphan'))

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

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
           'movie_id': self.movie_id,
           'actor_id': self.actor_id
        }
    
    def to_json(self):
        return {
            "movie_id_int": int(self.movie_id_int),
            "actor_id_int": int(self.actor_id_int)
        }   

IMG_URL = 'https://i.ibb.co/'

# insert default data

movie1 = Movie(id=1, title='Black Panther', release_date='2018-01-29', movie_img=IMG_URL+'xgNj30x/blackpanther.jpg', movie_publish=True)
movie2 = Movie(id=2, title='Jetsons: The Movie', release_date='1990-06-07', movie_img=IMG_URL+'w44pmy7/jetsons.jpg', movie_publish=True)
movie3 = Movie(id=3, title='Star Wars', release_date='1977-03-25', movie_img=IMG_URL+'0ryBFpX/starwars.jpg', movie_publish=True)
movie4 = Movie(id=4, title='Star Wars: The Force Awakens', release_date='2015-01-18', movie_img=IMG_URL+'87VCXRQ/forceawakens.jpg', movie_publish=True)
movie5 = Movie(id=5, title='WALL-E', release_date='2008-06-23', movie_img=IMG_URL+'brXh4kZ/wallefilm.jpg', movie_publish=True)
movie6 = Movie(id=6, title='Futurama', release_date='1999-03-28', movie_img=IMG_URL+'jVnjtz4/futurama.jpg', movie_publish=True)

actor1 = Actor(id=1, first_name='Panther', last_name='Robot', gender='robot', birth_date='1992-01-01', actor_img=IMG_URL+'zSwNG40/panther.jpg', actor_publish=True)
actor2 = Actor(id=2, first_name='Rosie', last_name='Robot', gender='gynoid', birth_date='2062-01-01', actor_img=IMG_URL+'60pLw3C/rosie.jpg', actor_publish=True)
actor3 = Actor(id=3, first_name='C-3PO', last_name='Droid', gender='droid', birth_date='7977-02-01', actor_img=IMG_URL+'GHGpcgf/c-3po.png', actor_publish=True)
actor4 = Actor(id=4, first_name='R2-D2', last_name='Droid', gender='droid', birth_date='7977-06-07', actor_img=IMG_URL+'NFvghgx/r2-d2.png', actor_publish=True)
actor5 = Actor(id=5, first_name='BB-8', last_name='Droid', gender='droid', birth_date='8006-01-01', actor_img=IMG_URL+'fVWFXSq/bb-8.jpg', actor_publish=True)
actor6 = Actor(id=6, first_name='WALL-E', last_name='Droid', gender='droid', birth_date='2805-12-31', actor_img=IMG_URL+'w4Qt7fG/wall-e.jpg', actor_publish=True)
actor7 = Actor(id=7, first_name='Bender', last_name='Bending Rodriguez', gender='other', birth_date='2996-09-24', actor_img=IMG_URL+'fpP8TDn/bender.jpg', actor_publish=True)

movieactor1 = MovieActorLink(movie_id=1, actor_id=1)
movieactor2 = MovieActorLink(movie_id=2, actor_id=2)
movieactor3 = MovieActorLink(movie_id=3, actor_id=3)
movieactor4 = MovieActorLink(movie_id=3, actor_id=4)
movieactor5 = MovieActorLink(movie_id=4, actor_id=3)
movieactor6 = MovieActorLink(movie_id=4, actor_id=4)
movieactor7 = MovieActorLink(movie_id=4, actor_id=5)
movieactor8 = MovieActorLink(movie_id=5, actor_id=6)
movieactor9 = MovieActorLink(movie_id=6, actor_id=7)

import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer, Date, ForeignKey, create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from flask_sqlalchemy.model import DefaultMeta
# from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship

db = SQLAlchemy()

BaseModel: DefaultMeta = db.Model


DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'picasso0')
DB_NAME = os.getenv('DB_NAME', 'castapp')

database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

engine = create_engine(database_path)

if database_exists(engine.url):
    drop_database(engine.url)
    create_database(engine.url)

#if not database_exists(engine.url):
else:
    create_database(engine.url)

print(database_exists(engine.url))

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
    !!NOTE you can change the database_filename variable to have multiple versions of a database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db.session.execute("ALTER SEQUENCE movies_id_seq RESTART WITH 1")
    db.session.execute("ALTER SEQUENCE actors_id_seq RESTART WITH 1")
    db.session.add_all([movie1, movie2, movie3]) 
    db.session.add_all([actor1, actor2, actor3]) 
    db.session.commit()
    db.session.add_all([movieactor1, movieactor2, movieactor3, movieactor4]) 
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
    release_date = db.Column(db.String(4), nullable=False) 
    actors = relationship('Actor', secondary='movie_actor_link')

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
    movies = relationship('Movie', secondary='movie_actor_link')

    def __init__(self, first_name, last_name, birth_date, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender

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
          'gender': self.gender}

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



# insert default data

movie1 = Movie(title='Steamboat Willie', release_date='1928')
movie2 = Movie(title='Wise Little Hen', release_date='1934')
movie3 = Movie(title='Fantasia', release_date='1940')

actor1 = Actor(first_name='Mickey', last_name='Mouse', gender='m', birth_date='1928-11-18')
actor2 = Actor(first_name='Minney', last_name='Mouse', gender='f', birth_date='1928-11-18')
actor3 = Actor(first_name='Donald', last_name='Duck', gender='m', birth_date='1934-06-09')

movieactor1 = MovieActorLink(movie_id=1, actor_id=1)
movieactor2 = MovieActorLink(movie_id=1, actor_id=2)
movieactor3 = MovieActorLink(movie_id=2, actor_id=3)
movieactor4 = MovieActorLink(movie_id=3, actor_id=1)

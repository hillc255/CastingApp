import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False

# DATABASE URL
DATABASE_URL = 'postgres://odsgqztiwmdgxb:fdba2f1e60653770f29df057aeedefd944889147582a10c8a4eb62883ab96ad6@ec2-544-167-152-185.compute-1.amazonaws.com:5432/d8gebjfq87smua'

#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:picasso0@localhost:5432/castapp'
SQLALCHEMY_DATABASE_URI = 'postgres://odsgqztiwmdgxb:fdba2f1e60653770f29df057aeedefd944889147582a10c8a4eb62883ab96ad6@ec2-544-167-152-185.compute-1.amazonaws.com:5432/d8gebjfq87smua'
import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False

# DATABASE URL
#old DATABASE_URL = 'postgres://odsgqztiwmdgxb:fdba2f1e60653770f29df057aeedefd944889147582a10c8a4eb62883ab96ad6@ec2-544-167-152-185.compute-1.amazonaws.com:5432/d8gebjfq87smua'
#DATABASE_URL = 'postgres://odsgqztiwmdgxb:fdba2f1e60653770f29df057aeedefd944889147582a10c8a4eb62883ab96ad6@ec2-54-167-152-185.compute-1.amazonaws.com:5432/d8gebjfq87smua'
DATABASE_URL = 'postgres://vxcrabcbgadapt:e580e6c5bcc3e7a410308bac6efb4ce8ef9636411c5368bab4b3bb6252c4119f@ec2-52-5-1-20.compute-1.amazonaws.com:5432/d4f05d6gpo6rhu'

#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:picasso0@localhost:5432/castapp'
#old SQLALCHEMY_DATABASE_URI = 'postgres://odsgqztiwmdgxb:fdba2f1e60653770f29df057aeedefd944889147582a10c8a4eb62883ab96ad6@ec2-544-167-152-185.compute-1.amazonaws.com:5432/d8gebjfq87smua'
#SQLALCHEMY_DATABASE_URI = 'postgres://odsgqztiwmdgxb:fdba2f1e60653770f29df057aeedefd944889147582a10c8a4eb62883ab96ad6@ec2-54-167-152-185.compute-1.amazonaws.com:5432/d8gebjfq87smua'
SQLALCHEMY_DATABASE_URI = 'postgres://vxcrabcbgadapt:e580e6c5bcc3e7a410308bac6efb4ce8ef9636411c5368bab4b3bb6252c4119f@ec2-52-5-1-20.compute-1.amazonaws.com:5432/d4f05d6gpo6rhu'

# class Config(object):
#     DEBUG = False
#     TESTING = False
#     CSRF_ENABLED = True
#     #SECRET_KEY = 'this-really-needs-to-be-changed'   
#     SECRET_KEY = os.urandom(32)
#     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


# class ProductionConfig(Config):
#     DEBUG = False


# class StagingConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class DevelopmentConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class TestingConfig(Config):
#     TESTING = True
import os

os.environ["SETTINGS_MODULE"] = 'settings'

# Example: uncomment format for local database path to test locally - unittest

# LOCAL_DATABASE_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
# '[user]','[password]', 'localhost:5432', '[database name]')
LOCAL_DATABASE_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    'postgres', 'picasso0', 'localhost:5432', 'castapp_test')

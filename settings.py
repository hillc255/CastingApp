import os 

# format for local database path to test postgres database with models
LOCAL_DATABASE_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format('postgres','picasso0', 'localhost:5432', 'castapp_test')
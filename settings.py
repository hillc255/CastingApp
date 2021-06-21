import os 

os.environ["SETTINGS_MODULE"] = 'settings' 

# Variables definition
# DATABASE_HOST = '00.0.0.0'
# DATABASE_NAME = 'DATABASENAME'

# format for local database path to test postgres database with models
LOCAL_DATABASE_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format('postgres','picasso0', 'localhost:5432', 'castapp_test')

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'picasso0')
DB_NAME = os.getenv('DB_NAME', 'castapp')
DB_URL = os.getenv('DB_URL', 'castapp')
APP_SETTINGS = os.getenv('APP_SETTING', 'config')




AUTH0_DOMAIN = 'autumn-voice-0666.us.auth0.com' # heroku auth0 domain + "/"
ALGORITHMS = ['RS256']
#API_AUDIENCE = 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj'
API_AUDIENCE = 'https://cast-app.herokuapp.com/api'
#API_AUDIENCE = 'cast-app' # heroku app name
           
ROLES_URI  = 'https://cast-app.herokuapp.com/roles'

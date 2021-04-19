import backend.src.app

waitress.serve(app.wsgifunc, port=8041, url_scheme='https')
heroku ps:scale web=1

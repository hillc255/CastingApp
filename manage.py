from flask_script import Manager
"""This file sets up a command line manager.
Use "python manage.py" for a list of available commands.
Use "python manage.py runserver" to start the development web server
 on localhost:5000.
Use "python manage.py runserver --help" for a list of runserver options.
"""

from flask_migrate import Migrate, MigrateCommand

from app import app
from backend.src.database.models import db

print(f"**** manage.py ****")

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

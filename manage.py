from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from api import admin
from api.models import db
from app import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


if __name__ == '__main__':
    manager.run()

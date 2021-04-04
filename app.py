import os

from flask import Flask

from api.api import api
from api.models import db
from api.serializers import ma

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api.init_app(app)
db.init_app(app)
ma.init_app(app)


def create_app(config_name):
    app = Flask(__name__,
                static_url_path='/static',
                static_folder='static')
    app.config.from_object(config_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    return app

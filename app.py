import os

from flask import Flask

from api.models import db

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

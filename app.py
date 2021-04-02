import os

from flask import Flask
from flask_restful import Api

from api.models import db
from api.resources import Book, Books
from api.serializers import ma

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')
api = Api(app)
api.add_resource(Books, '/api/v1/books/')
api.add_resource(Book, '/api/v1/books/<int:book_id>/')

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)

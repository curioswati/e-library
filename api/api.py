from flask_restful import Api

from api.resources import Book, Books, User, Users

api = Api()
api.add_resource(Books, '/api/v1/books/')
api.add_resource(Book, '/api/v1/books/<int:book_id>/')
api.add_resource(Users, '/api/v1/users/')
api.add_resource(User, '/api/v1/users/<int:user_id>/')

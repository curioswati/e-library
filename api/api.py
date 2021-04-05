from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api

from api.resources import Book, Books, Transaction, Transactions, User, Users

api = Api()
api.add_resource(Books, '/api/v1/books/', '/api/v1/books/<popular>/')
api.add_resource(Book, '/api/v1/books/<int:book_id>/')
api.add_resource(Users, '/api/v1/users/', '/api/v1/users/<highest_paying>/')
api.add_resource(User, '/api/v1/users/<int:user_id>/')
api.add_resource(Transactions, '/api/v1/transactions/')
api.add_resource(Transaction, '/api/v1/transactions/<int:transaction_id>/')

docs = FlaskApiSpec()
docs.register(Book)
docs.register(Books)
docs.register(User)
docs.register(Users)
docs.register(Transaction)
docs.register(Transactions)

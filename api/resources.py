from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api.decorators import validate_request_data
from api.messages import STATUS_404, STATUS_405, STATUS_409
from api.serializers import book_schema, transaction_schema, user_schema
from api.services import BookService, TransactionService, UserService


class Book(Resource, BookService):
    def get(self, book_id=None):
        book = self.get_book(book_id)

        if not book:
            abort(404, message=STATUS_404)

        return book, 200

    @validate_request_data(book_schema, partial=True)
    def put(self, book_id):
        request_data = request.get_json()

        book = self.update_book(book_id, request_data)
        if book:
            return book['url'], 201
        else:
            return '', 204

    def delete(self, book_id):
        book_id = self.delete_book(book_id)

        if book_id:
            return book_id, 200
        else:
            abort(404, message=STATUS_404)


class Books(Resource, BookService):
    def get(self):
        return self.get_books()

    @validate_request_data(book_schema, partial=False)
    def post(self):
        request_data = request.get_json()

        try:
            book = self.add_book(request_data)
        except IntegrityError as e:
            abort(409, message=STATUS_409 % e.message)
        else:
            return book['url'], 201


class User(Resource, UserService):
    def get(self, user_id=None):
        user = self.get_user(user_id)

        if not user:
            abort(404, message=STATUS_404)

        return user, 200

    @validate_request_data(user_schema, partial=True)
    def put(self, user_id):
        request_data = request.get_json()

        user = self.update_user(user_id, request_data)
        if user:
            return user['url'], 201
        else:
            return '', 204

    def delete(self, user_id):
        user_id = self.delete_user(user_id)

        if user_id:
            return user_id, 200
        else:
            abort(404, message=STATUS_404)


class Users(Resource, UserService):
    def get(self):
        return self.get_users()

    @validate_request_data(user_schema, partial=False)
    def post(self):
        request_data = request.get_json()

        try:
            user = self.add_user(request_data)
        except IntegrityError as e:
            abort(409, message=STATUS_409 % e.message)
        else:
            return user['url'], 201


class Transaction(Resource, TransactionService):
    def get(self, transaction_id=None):
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            abort(404, message=STATUS_404)

        return transaction, 200

    @validate_request_data(transaction_schema, partial=True)
    def put(self, transaction_id):
        if request.json or request.data:
            abort(405, message=STATUS_405)

        try:
            self.update_transaction(transaction_id)
        except NoResultFound:
            abort(404, message=STATUS_404)
        else:
            return '', 204


class Transactions(Resource, TransactionService):
    def get(self):
        return self.get_transactions()

    @validate_request_data(transaction_schema, partial=True)
    def post(self):
        request_data = request.get_json()

        try:
            transaction = self.add_transaction(request_data)
        except ValueError as e:
            abort(409, message=e.args[0])
        else:
            return transaction['url'], 201

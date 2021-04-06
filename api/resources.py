from flask import request
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api.constants import BOOKS_ENDPOINT, TRANSACTIONS_ENDPOINT, USERS_ENDPOINT
from api.decorators import validate_request_data
from api.messages import STATUS_404, STATUS_405, STATUS_409
from api.serializers import (BookSchema, ResponseSchema, TransactionSchema,
                             UserSchema)
from api.services import BookService, TransactionService, UserService


class Book(MethodResource, Resource, BookService):
    @marshal_with(BookSchema)
    def get(self, book_id=None):
        book = self.get_book(book_id)

        if not book:
            abort(404, message=STATUS_404)

        return book, 200

    @marshal_with(ResponseSchema, code=204)
    @validate_request_data(BookSchema(), partial=True)
    def put(self, book_id):
        request_data = request.get_json()

        book = self.update_book(book_id, request_data)
        if book:
            return {'url': f'{BOOKS_ENDPOINT}/{str(book.id)}/'}, 201
        else:
            return '', 204

    @marshal_with(ResponseSchema)
    def delete(self, book_id):
        book_id = self.delete_book(book_id)

        if book_id:
            return book_id, 200
        else:
            abort(404, message=STATUS_404)


class Books(MethodResource, Resource, BookService):
    @marshal_with(BookSchema(many=True))
    def get(self, request_type=None):
        return self.get_books(request_type, **request.args)

    @marshal_with(ResponseSchema)
    @validate_request_data(BookSchema(), partial=False)
    def post(self):
        request_data = request.get_json()

        try:
            book = self.add_book(request_data)
        except IntegrityError as e:
            abort(409, message=STATUS_409 % e.message)
        else:
            return {'url': f'{BOOKS_ENDPOINT}/{str(book.id)}/'}, 201


class User(MethodResource, Resource, UserService):
    @marshal_with(UserSchema)
    def get(self, user_id=None):
        user = self.get_user(user_id)

        if not user:
            abort(404, message=STATUS_404)

        return user, 200

    @marshal_with(ResponseSchema)
    @validate_request_data(UserSchema(), partial=True)
    def put(self, user_id):
        request_data = request.get_json()

        user = self.update_user(user_id, request_data)
        if user:
            return {'url': f'{USERS_ENDPOINT}/{str(user.id)}/'}, 201
        else:
            return '', 204

    @marshal_with(ResponseSchema)
    def delete(self, user_id):
        user_id = self.delete_user(user_id)

        if user_id:
            return user_id, 200
        else:
            abort(404, message=STATUS_404)


class Users(MethodResource, Resource, UserService):
    @marshal_with(UserSchema(many=True))
    def get(self, highest_paying=False):
        limit = request.args.get('limit')
        return self.get_users(highest_paying, limit)

    @marshal_with(ResponseSchema)
    @validate_request_data(UserSchema(), partial=False)
    def post(self):
        request_data = request.get_json()

        try:
            user = self.add_user(request_data)
        except IntegrityError as e:
            abort(409, message=STATUS_409 % e.message)
        else:
            return {'url': f'{USERS_ENDPOINT}/{str(user.id)}/'}, 201


class Transaction(MethodResource, Resource, TransactionService):
    @marshal_with(TransactionSchema)
    def get(self, transaction_id=None):
        transaction = self.get_transaction(transaction_id)

        if not transaction:
            abort(404, message=STATUS_404)

        return transaction, 200

    @marshal_with(ResponseSchema)
    @validate_request_data(TransactionSchema(), partial=True)
    def put(self, transaction_id):
        if request.json or request.data:
            abort(405, message=STATUS_405)

        try:
            self.update_transaction(transaction_id)
        except NoResultFound:
            abort(404, message=STATUS_404)
        else:
            return '', 204


class Transactions(MethodResource, Resource, TransactionService):
    @marshal_with(TransactionSchema(many=True))
    def get(self):
        return self.get_transactions()

    @marshal_with(ResponseSchema)
    @validate_request_data(TransactionSchema(), partial=True)
    def post(self):
        request_data = request.get_json()

        try:
            transaction = self.add_transaction(request_data)
        except ValueError as e:
            abort(409, message=e.args[0])
        else:
            return {'url': f'{TRANSACTIONS_ENDPOINT}/{str(transaction.id)}/'}, 201

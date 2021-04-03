from flask import request
from flask_restful import Resource, abort
from werkzeug.exceptions import BadRequest

from api.serializers import book_schema
from api.services import BookService


class Book(Resource, BookService):
    def get(self, book_id=None):
        return self.get_book(book_id)

    def put(self, book_id):
        try:
            request_data = request.get_json()
        except BadRequest:
            abort(400, message="Invalid Data")

        data_errors = book_schema.validate(request_data, partial=True)
        if data_errors:
            abort(400, message=data_errors)

        book = self.update_book(book_id, request_data)
        if book:
            return book['url'], 201
        else:
            return '', 204

    def delete(self, book_id):
        book_id = self.delete_book(book_id)
        return book_id, 200


class Books(Resource, BookService):
    def get(self):
        return self.get_books()

    def post(self):
        book = self.add_book(request.get_json())

class User(Resource, UserService):
    def get(self, user_id=None):
        user = self.get_user(user_id)

        if not user:
            abort(404, message=STATUS_404)

        return user, 200

    def put(self, user_id):
        try:
            request_data = request.get_json()
        except BadRequest:
            abort(400, message=STATUS_400)

        data_errors = user_schema.validate(request_data, partial=True)
        if data_errors:
            abort(400, message=data_errors)

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

    def post(self):
        request_data = request.get_json()

        try:
            user = self.add_user(request_data)
        except IntegrityError as e:
            abort(409, message=STATUS_409 % e.message)
        else:
            return user['url'], 201

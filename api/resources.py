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

        if book:
            book_serialized = book_schema.dump(book)
            abort(409, message=f"Book already exists: {book_serialized['url']}")

        return book['url'], 201

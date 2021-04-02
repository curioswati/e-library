from sqlalchemy.exc import IntegrityError

from api.models import Book, db
from api.serializers import book_schema


class BookService():
    '''
    Bridge between book resource and model.
    '''
    def get_books(self):
        books = Book.query.all()
        books_serialized = [book_schema.dump(book) for book in books]
        return books_serialized

    def get_book(self, book_id):
        book = Book.query.get(book_id)
        book_serialized = book_schema.dump(book)

        return book_serialized

    def add_book(self, book_json):
        new_book = book_schema.load(book_json)

        try:
            db.session.add(new_book)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            existing_book = Book.query.filter_by(isbn=book_json['isbn']).one()
            book_serialized = book_schema.dump(existing_book)
            return book_serialized
        else:
            return

    def update_book(self, book_id, data):
        existing_book = Book.query.get(book_id)

        if not existing_book:
            new_book = book_schema.load(data)
            db.session.add(new_book)
            db.session.commit()

            book_serialized = book_schema.dump(new_book)
            return book_serialized

        else:
            if 'title' in data:
                existing_book.title = data.pop('title')
            if 'isbn' in data:
                existing_book.isbn = data.pop('isbn')
            if 'author' in data:
                existing_book.author = data.pop('author')
            if 'price' in data:
                existing_book.price = data.pop('price')
            if 'stock' in data:
                existing_book.stock = data.pop('stock')

            db.session.add(existing_book)
            db.session.commit()
            return

    def delete_book(self, book_id):
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()

        return book.id

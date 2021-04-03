from sqlalchemy.exc import IntegrityError

from api.models import Book, User, db
from api.serializers import book_schema, user_schema


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

        if book:
            book_serialized = book_schema.dump(book)
            return book_serialized
        return

    def add_book(self, book_json):
        new_book = book_schema.load(book_json)

        try:
            db.session.add(new_book)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()

            existing_book = Book.query.filter_by(isbn=book_json['isbn']).one()
            book_serialized = book_schema.dump(existing_book)

            e.message = book_serialized['url']
            raise e
        else:
            book_serialized = book_schema.dump(new_book)
            return book_serialized

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

        if book:
            db.session.delete(book)
            db.session.commit()
            return book.id
        return


class UserService():
    '''
    Bridge between user resource and model.
    '''
    def get_users(self):
        users = User.query.all()
        users_serialized = [user_schema.dump(user) for user in users]
        return users_serialized

    def get_user(self, user_id):
        user = User.query.get(user_id)

        if user:
            user_serialized = user_schema.dump(user)
            return user_serialized
        return

    def add_user(self, user_json):
        new_user = user_schema.load(user_json)

        try:
            db.session.add(new_user)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()

            existing_user = User.query.filter_by(email=user_json['email']).one()
            user_serialized = user_schema.dump(existing_user)

            e.message = user_serialized['url']
            raise e
        else:
            user_serialized = user_schema.dump(new_user)
            return user_serialized

    def update_user(self, user_id, data):
        existing_user = User.query.get(user_id)

        if not existing_user:
            new_user = user_schema.load(data)
            db.session.add(new_user)
            db.session.commit()

            user_serialized = user_schema.dump(new_user)
            return user_serialized

        else:
            if 'email' in data:
                existing_user.email = data.pop('email')
            if 'first_name' in data:
                existing_user.first_name = data.pop('first_name')
            if 'last_name' in data:
                existing_user.last_name = data.pop('last_name')
            if 'contact' in data:
                existing_user.contact = data.pop('contact')

            db.session.add(existing_user)
            db.session.commit()
            return

    def delete_user(self, user_id):
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
            return user.id
        return

from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api.constants import MAX_ALLOWED_DUE
from api.messages import OUT_OF_STOCK, OVERDUE, STOCK_SHORTAGE
from api.models import Book, Transaction, User, db
from api.serializers import book_schema, transaction_schema, user_schema


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


class TransactionService():
    '''
    Bridge between transaction resource and model.
    '''
    def get_transactions(self):
        transactions = Transaction.query.all()
        transactions_serialized = [
                transaction_schema.dump(transaction) for transaction in transactions
        ]
        return transactions_serialized

    def get_transaction(self, transaction_id):
        transaction = Transaction.query.get(transaction_id)

        if transaction:
            transaction_serialized = transaction_schema.dump(transaction)
            return transaction_serialized
        return

    def add_transaction(self, transaction_json):
        book_id = transaction_json.get('book')
        member_id = transaction_json.get('book')
        num_copies = int(transaction_json.get('num_copies'))

        member_occupied_books = Transaction.query.filter_by(
                                                            member=member_id,
                                                            date_return=None
                                                            )
        total_due = sum([int(book.rent) for book in member_occupied_books])
        if total_due > MAX_ALLOWED_DUE:
            raise ValueError(OVERDUE)

        book = Book.query.get(book_id)
        if not book.stock:
            raise ValueError(OUT_OF_STOCK)
        elif book.stock < num_copies:
            raise ValueError(STOCK_SHORTAGE % book.stock)
        else:
            book.stock -= int(num_copies)

        rent = num_copies * book.price
        transaction_json['rent'] = rent
        new_transaction = transaction_schema.load(transaction_json)
        db.session.add(new_transaction)
        db.session.add(book)
        db.session.commit()

        transaction_serialized = transaction_schema.dump(new_transaction)
        return transaction_serialized

    def update_transaction(self, transaction_id):
        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            raise NoResultFound

        book = Book.query.get(transaction.book)
        num_copies = transaction.num_copies

        book.stock += num_copies
        transaction.date_return = datetime.now()
        db.session.add(transaction)
        db.session.add(book)
        db.session.commit()
        return

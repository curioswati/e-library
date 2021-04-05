from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.functions import func

from api.constants import DEFAULT_RESULT_LIMIT, MAX_ALLOWED_DUE
from api.messages import OUT_OF_STOCK, OVERDUE, STOCK_SHORTAGE
from api.models import Book, Transaction, User, db
from api.serializers import book_schema, transaction_schema, user_schema


class BookService():
    '''
    Bridge between book resource and model.
    '''
    def get_popular_books(self, limit=DEFAULT_RESULT_LIMIT):
        # Ref: https://stackoverflow.com/q/27900018
        books = Book.query.join(Transaction, Book.id == Transaction.book, isouter=True)\
               .group_by(Book)\
               .order_by(desc(func.count(Transaction.book)))\
               .limit(limit).all()
        return books

    def search_book(self, title, author):
        if title and author:
            books = Book.query.filter(Book.title.like(f'%{title}%'),
                                      Book.author.like(f'%{author}%')
                                      ).all()
        elif title:
            books = Book.query.filter(Book.title.like(f'%{title}%')).all()
        elif author:
            books = Book.query.filter(Book.author.like(f'%{author}%')).all()
        return books

    def get_books(self, request_type, **kwargs):
        if request_type == 'popular':
            limit = kwargs.get('limit')
            books = self.get_popular_books(limit)

        elif request_type == 'search':
            title = kwargs.get('title')
            author = kwargs.get('author')
            books = self.search_book(title, author)

        else:
            books = Book.query.all()

        return books

    def get_book(self, book_id):
        book = Book.query.get(book_id)
        return book

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
            return new_book

    def update_book(self, book_id, data):
        existing_book = Book.query.get(book_id)

        if not existing_book:
            new_book = book_schema.load(data)
            db.session.add(new_book)
            db.session.commit()

            return new_book

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
    def get_users(self, highest_paying, limit):
        if highest_paying:
            # Ref: https://stackoverflow.com/q/27900018
            users = User.query.join(Transaction, User.id == Transaction.member, isouter=True)\
                   .group_by(User)\
                   .order_by(desc(func.sum(Transaction.rent)))\
                   .limit(limit).all()
        else:
            users = User.query.all()
        return users

    def get_user(self, user_id):
        user = User.query.get(user_id)
        return user

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
            return new_user

    def update_user(self, user_id, data):
        existing_user = User.query.get(user_id)

        if not existing_user:
            new_user = user_schema.load(data)
            db.session.add(new_user)
            db.session.commit()
            return new_user

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
        return transactions

    def get_transaction(self, transaction_id):
        transaction = Transaction.query.get(transaction_id)

        return transaction

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

        return new_transaction

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

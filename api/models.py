from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    '''
    Member of the library.
    '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    contact = db.Column(db.String(10), nullable=False)

    def __init__(self, email, first_name, last_name, contact):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Book(db.Model):
    '''
    Book in the library.
    '''

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer(), default=30)
    stock = db.Column(db.Integer, default=1)

    def __init__(self, title, isbn, author, stock, price):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.stock = stock
        self.price = price

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Transaction(db.Model):
    '''
    Rent transactions done by members on books.
    '''

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    date_rented = db.Column(db.DateTime, nullable=False)
    date_return = db.Column(db.DateTime)

    def __init__(self, member, book, rent, date_rented, date_return):
        self.member = member
        self.book = book
        self.rent = rent
        self.date_rented = date_rented
        self.date_return = date_return

    def __repr__(self):
        return '<id {}>'.format(self.id)

from flask_marshmallow import Marshmallow
from marshmallow import post_load

from api.models import Book, User

ma = Marshmallow()


class BookSchema(ma.SQLAlchemyAutoSchema):
    '''
    Serializes book from and to DB.
    '''
    class Meta:
        model = Book
        include_fk = True

    url = ma.URLFor('book', values=dict(book_id='<id>'))

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)


class UserSchema(ma.SQLAlchemyAutoSchema):
    '''
    Serializes book from and to DB.
    '''
    class Meta:
        model = User
        include_fk = True

    url = ma.URLFor('user', values=dict(user_id='<id>'))

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


book_schema = BookSchema()
user_schema = UserSchema()

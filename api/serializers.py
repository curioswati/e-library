from flask_marshmallow import Marshmallow
from marshmallow import post_load

from api.models import Book

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


book_schema = BookSchema()

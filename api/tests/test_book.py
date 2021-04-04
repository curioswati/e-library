import re
import unittest

from api.models import Book, db
from api.serializers import book_schema
from app import create_app


class BookResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()

        self.book = Book(
            title='Lean In',
            isbn='0385349949',
            author='Sheryl Sandberg',
            stock=5,
            price=30
        )

        with self.app.app_context():
            db.create_all()

            db.session.add(self.book)
            db.session.commit()

    def test_get_book_200(self):
        # When
        response = self.client.get('/api/v1/books/1/')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertFalse(book_schema.validate(response.json))

    def test_get_book_404(self):
        # When
        response = self.client.get('/api/v1/books/2/')

        # Then
        self.assertEqual(404, response.status_code)

    def test_get_books(self):
        # When
        response = self.client.get('/api/v1/books/')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json))
        self.assertFalse(book_schema.validate(response.json[0]))

    def test_post_book_201(self):
        # Given
        data = {
            "stock": 5,
            "author": "Some Author",
            "isbn": "1385349947",
            "title": "Some Title",
            "price": 30
        }

        # When
        response = self.client.post('/api/v1/books/', json=data)

        # Then
        self.assertEqual(201, response.status_code)
        assert re.match(r'/api/v1/books/\d+/', response.json)

    def test_post_book_400(self):
        # Given
        data = {
            "stock": 5,
            "author": "Some Author",
            "isbn": "1385349947",
            "price": 30
        }

        # When
        response = self.client.post('/api/v1/books/', json=data)

        # Then
        self.assertEqual(400, response.status_code)

    def test_post_book_409(self):
        # Given
        data = {
            "stock": 3,
            "author": "Sheryl Sandberg",
            "isbn": "0385349949",
            "title": "Lean In",
            "price": 50
        }

        # When
        response = self.client.post('/api/v1/books/', json=data)

        # Then
        self.assertEqual(409, response.status_code)

    def test_put_book_400(self):
        # Given
        data = {"title": 5}

        # When
        response = self.client.put(f'/api/v1/books/1/', json=data)

        # Then
        self.assertEqual(400, response.status_code)

    def test_put_book_204(self):
        # Given
        data = {"stock": 5}

        # When
        response = self.client.put(f'/api/v1/books/1/', json=data)

        # Then
        self.assertEqual(204, response.status_code)

    def test_put_book_201(self):
        # Given
        data = {
            "stock": 5,
            "author": "Some Author",
            "isbn": "1385349947",
            "title": "Some Title",
            "price": 30
        }

        # When
        response = self.client.put(f'/api/v1/books/2/', json=data)

        # Then
        self.assertEqual(201, response.status_code)
        assert re.match(r'/api/v1/books/\d+/', response.json)

    def test_delete_book_200(self):
        # When
        response = self.client.delete(f'/api/v1/books/1/')

        # Then
        self.assertEqual(200, response.status_code)

    def test_delete_book_404(self):
        # When
        response = self.client.delete(f'/api/v1/books/2/')

        # Then
        self.assertEqual(404, response.status_code)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

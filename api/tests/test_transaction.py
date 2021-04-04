import re
import unittest
from datetime import datetime

from api.messages import STOCK_SHORTAGE
from api.models import Book, Transaction, User, db
from api.serializers import transaction_schema
from app import create_app


class TransactionResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()

        self.user = User(
            email='abc@example.com',
            first_name='First',
            last_name='Last',
            contact='1234567890',
        )

        self.book = Book(
            title='Lean In',
            isbn='0385349949',
            author='Sheryl Sandberg',
            stock=5,
            price=30
        )

        self.transaction = Transaction(
            member=1,
            book=1,
            num_copies=2,
            rent=60,
            date_rented=datetime.now()
        )

        with self.app.app_context():
            db.create_all()

            db.session.add(self.user)
            db.session.add(self.book)
            db.session.add(self.transaction)
            db.session.commit()

    def test_get_transaction_200(self):
        # When
        response = self.client.get('/api/v1/transactions/1/')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertFalse(transaction_schema.validate(response.json))

    def test_get_transaction_404(self):
        # When
        response = self.client.get('/api/v1/transactions/2/')

        # Then
        self.assertEqual(404, response.status_code)

    def test_get_transactions(self):
        # When
        response = self.client.get('/api/v1/transactions/')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json))
        self.assertFalse(transaction_schema.validate(response.json[0]))

    def test_post_transaction_201(self):
        # Given
        data = {
            "book": 1,
            "member": 1,
            "num_copies": 2,
        }

        # When
        response = self.client.post('/api/v1/transactions/', json=data)

        with self.app.app_context():
            book = Book.query.get(1)
            self.assertEqual(book.stock, 3)

        # Then
        self.assertEqual(201, response.status_code)
        assert re.match(r'/api/v1/transactions/\d+/', response.json)

    def test_post_transaction_409(self):
        # Given
        data = {
            "book": 1,
            "member": 1,
            "num_copies": 6,
        }

        # When
        response = self.client.post('/api/v1/transactions/', json=data)

        # Then
        self.assertEqual(409, response.status_code)

        with self.app.app_context():
            book = Book.query.get(1)
            self.assertEqual(STOCK_SHORTAGE % book.stock, response.json['message'])

    def test_put_transaction_204(self):
        # Given
        data = {}

        # When
        response = self.client.put(f'/api/v1/transactions/1/', json=data)

        # Then
        self.assertEqual(204, response.status_code)

        with self.app.app_context():
            transaction = Transaction.query.get(1)
            self.assertEqual(transaction.date_return.date(),
                             datetime.now().today().date())

    def test_put_transaction_404(self):
        # Given
        data = {}

        # When
        response = self.client.put(f'/api/v1/transactions/2/', json=data)

        # Then
        self.assertEqual(404, response.status_code)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

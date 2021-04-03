import re
import unittest

from api.models import User, db
from api.serializers import user_schema
from app import create_app


class UserResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()

        self.user = User(
            email='abc@example.com',
            first_name='First',
            last_name='Last',
            contact='1234567890',
        )

        with self.app.app_context():
            db.create_all()

            db.session.add(self.user)
            db.session.commit()

    def test_get_user_success(self):
        # When
        response = self.client.get('/api/v1/users/1/')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertFalse(user_schema.validate(response.json))

    def test_get_user_404(self):
        # When
        response = self.client.get('/api/v1/users/2/')

        # Then
        self.assertEqual(404, response.status_code)

    def test_get_users(self):
        # When
        response = self.client.get('/api/v1/users/')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json))
        self.assertFalse(user_schema.validate(response.json[0]))

    def test_post_user_success(self):
        # Given
        data = {
            "email": "xyz@example.com",
            "first_name": "Some",
            "last_name": "Author",
            "contact": "1234567890",
        }

        # When
        response = self.client.post('/api/v1/users/', json=data)

        # Then
        self.assertEqual(201, response.status_code)
        assert re.match(r'/api/v1/users/\d+/', response.json)

    def test_post_user_400(self):
        # Given
        data = {
            "email": "xyz@example.com",
            "first_name": "Some",
            "last_name": "Author",
        }

        # When
        response = self.client.post('/api/v1/users/', json=data)

        # Then
        self.assertEqual(400, response.status_code)

    def test_post_user_409(self):
        # Given
        data = {
            "email": "abc@example.com",
            "first_name": "Some",
            "last_name": "Author",
            "contact": "1234567890",
        }

        # When
        response = self.client.post('/api/v1/users/', json=data)

        # Then
        self.assertEqual(409, response.status_code)

    def test_put_user_400(self):
        # Given
        data = {"email": 5}

        # When
        response = self.client.put(f'/api/v1/users/1/', json=data)

        # Then
        self.assertEqual(400, response.status_code)

    def test_put_user_204(self):
        # Given
        data = {"contact": "9012345678"}

        # When
        response = self.client.put(f'/api/v1/users/1/', json=data)

        # Then
        self.assertEqual(204, response.status_code)

    def test_put_user_201(self):
        # Given
        data = {
            "email": "xyz@example.com",
            "first_name": "Some",
            "last_name": "Author",
            "contact": "1234567890",
        }

        # When
        response = self.client.put(f'/api/v1/users/2/', json=data)

        # Then
        self.assertEqual(201, response.status_code)
        assert re.match(r'/api/v1/users/\d+/', response.json)

    def test_delete_user_success(self):
        # When
        response = self.client.delete(f'/api/v1/users/1/')

        # Then
        self.assertEqual(200, response.status_code)

    def test_delete_user_404(self):
        # When
        response = self.client.delete(f'/api/v1/users/2/')

        # Then
        self.assertEqual(404, response.status_code)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

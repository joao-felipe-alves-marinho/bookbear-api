import json

from django.test import AsyncClient

from BookBearApi.tests.config import TestCaseWithData


class TestAuthController(TestCaseWithData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = '/api/v1/auth/'

    async def test_user_registration(self):
        client = AsyncClient()
        payload = json.dumps({
            'email': 'user@gmail.com',
            'username': 'user',
            'password': 'user',
            'birth_date': '2000-01-01',
            'gender': 'MC'
        })
        form = {
            'avatar': '',
            'payload': payload
        }
        response = await client.post(
            path=self.url + 'register',
            data=form
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['username'], 'user')
        self.assertEqual(response.json()['email'], 'user@gmail.com')

    async def test_user_authentication(self):
        client = AsyncClient()
        response = await client.post(
            path=self.url + 'login',
            data=json.dumps({
                'username': 'user1@gmail.com',
                'password': 'user1'
            }),
            content_type='application/json',
        )
        user = response.json()['user']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user['username'], 'user1')
        self.assertEqual(user['email'], 'user1@gmail.com')
        self.assertIn('access', response.json())

    async def test_user_authentication_invalid(self):
        client = AsyncClient()
        response = await client.post(
            path=self.url + 'login',
            data=json.dumps({
                'username': 'user1@gmail.com',
                'password': 'abc12345'
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Incorrect Credentials')

    async def test_user_logout(self):
        response = await self.client_auth.post(
            path=self.url + 'logout',
            data=json.dumps({
                'refresh': self.access_token
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'success')

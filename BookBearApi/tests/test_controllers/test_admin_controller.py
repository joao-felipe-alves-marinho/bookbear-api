import json

from asgiref.sync import async_to_sync
from django.test import AsyncClient

from BookBearApi.tests.config import TestCaseWithData


class TestAdminController(TestCaseWithData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = '/api/v1/admin/'
        cls.access_token_admin = async_to_sync(cls.get_access_token_admin)()
        cls.client_auth_admin = AsyncClient(AUTHORIZATION=f'Bearer {cls.access_token_admin}')

    @classmethod
    async def get_access_token_admin(cls):
        client = AsyncClient()
        response_token = await client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'username': 'admin@gmail.com',
                'password': 'admin'
            }),
            content_type='application/json',
        )
        return response_token.json()['access']

    async def test_create_book(self):
        payload = json.dumps({
            'title': 'Book',
            'publication_date': '2000-01-01',
            'age_rating': 'E',
            'publisher': 1,
            'authors': [1],
            'genres': [1, 2]
        })
        form = {
            'cover': '',
            'payload': payload
        }
        response = await self.client_auth_admin.post(
            path=self.url + 'book',
            data=form,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], 'Book')
        self.assertEqual(response.json()['publication_date'], '2000-01-01')
        self.assertEqual(response.json()['age_rating'], 'E')
        self.assertEqual(response.json()['publisher']['id'], 1)
        self.assertEqual(response.json()['publisher']['name'], 'Publisher 1')
        self.assertEqual(response.json()['authors'][0]['id'], 1)
        self.assertEqual(response.json()['authors'][0]['name'], 'Author 1')
        self.assertEqual(response.json()['genres'][0]['id'], 1)
        self.assertEqual(response.json()['genres'][0]['name'], 'Genre 1')

    async def test_update_book(self):
        response = await self.client_auth_admin.patch(
            path=self.url + 'book/1',
            data=json.dumps({
                'title': 'Book 100',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Book 100')

    async def test_delete_book(self):
        response = await self.client_auth_admin.delete(
            path=self.url + 'book/1',
        )
        self.assertEqual(response.status_code, 204)

    async def test_create_author(self):
        payload = json.dumps({
            'name': 'Author',
            'birth_date': '2000-01-01',
        })
        form = {
            'avatar': '',
            'payload': payload
        }
        response = await self.client_auth_admin.post(
            path=self.url + 'author',
            data=form,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Author')
        self.assertEqual(response.json()['birth_date'], '2000-01-01')

    async def test_update_author(self):
        response = await self.client_auth_admin.patch(
            path=self.url + 'author/1',
            data=json.dumps({
                'name': 'Author 100',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Author 100')

    async def test_delete_author(self):
        response = await self.client_auth_admin.delete(
            path=self.url + 'author/1',
        )
        self.assertEqual(response.status_code, 204)

    async def test_create_publisher(self):
        payload = json.dumps({
            'name': 'Publisher',
        })
        form = {
            'logo': '',
            'payload': payload
        }
        response = await self.client_auth_admin.post(
            path=self.url + 'publisher',
            data=form,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Publisher')

    async def test_update_publisher(self):
        response = await self.client_auth_admin.patch(
            path=self.url + 'publisher/1',
            data=json.dumps({
                'name': 'Publisher 100',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Publisher 100')

    async def test_delete_publisher(self):
        response = await self.client_auth_admin.delete(
            path=self.url + 'publisher/1',
        )
        self.assertEqual(response.status_code, 204)

    async def test_create_genre(self):
        response = await self.client_auth_admin.post(
            path=self.url + 'genre',
            data=json.dumps({
                'name': 'Genre',
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Genre')

    async def test_update_genre(self):
        response = await self.client_auth_admin.patch(
            path=self.url + 'genre/1',
            data=json.dumps({
                'name': 'Genre 100',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Genre 100')

    async def test_delete_genre(self):
        response = await self.client_auth_admin.delete(
            path=self.url + 'genre/1',
        )
        self.assertEqual(response.status_code, 204)

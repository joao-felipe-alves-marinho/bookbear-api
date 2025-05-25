import json

from BookBearApi.tests.config import TestCaseWithData


class TestUserController(TestCaseWithData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = '/api/v1/user/'

    async def test_get_user(self):
        response = await self.client_auth.get(
            path=self.url + 'me'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'user1')
        self.assertEqual(response.json()['email'], 'user1@gmail.com')

    async def test_get_user_by_id(self):
        response = await self.client_auth.get(
            path=self.url + '2',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'user2')
        self.assertEqual(response.json()['email'], 'user2@gmail.com')

    async def test_update_user(self):
        response = await self.client_auth.patch(
            path=self.url + 'me',
            data=json.dumps({
                'username': 'user100'
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'user100')
        self.assertEqual(response.json()['email'], 'user1@gmail.com')

    async def test_delete_user(self):
        response = await self.client_auth.delete(
            path=self.url + 'me'
        )
        self.assertEqual(response.status_code, 204)

    async def test_get_user_books(self):
        response = await self.client_auth.get(
            path=self.url + 'books'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['situation'], 'C')
        self.assertEqual(response.json()[0]['rating'], 5)
        self.assertEqual(response.json()[0]['review'], 'Review of the book')
        self.assertIn('book', response.json()[0])
        self.assertEqual(response.json()[1]['situation'], 'R')
        self.assertEqual(response.json()[1]['rating'], None)
        self.assertEqual(response.json()[1]['review'], '')
        self.assertIn('book', response.json()[1])

    async def test_add_user_book(self):
        response = await self.client_auth.post(
            path=self.url + 'books/1',
            data=json.dumps({
                'situation': 'C',
                'rating': 5,
                'review': 'Review of the book'
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['situation'], 'C')
        self.assertEqual(response.json()['rating'], 5)
        self.assertEqual(response.json()['review'], 'Review of the book')
        self.assertIn('book', response.json())

    async def test_update_user_book(self):
        response = await self.client_auth.patch(
            path=self.url + 'books/2',
            data=json.dumps({
                'rating': 4,
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['situation'], 'C')
        self.assertEqual(response.json()['rating'], 4)
        self.assertEqual(response.json()['review'], 'Review of the book')
        self.assertIn('book', response.json())

    async def test_delete_user_book(self):
        response = await self.client_auth.delete(
            path=self.url + 'books/2'
        )
        self.assertEqual(response.status_code, 204)

    async def test_add_user_genre(self):
        response = await self.client_auth.post(
            path=self.url + 'genres/1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['favorite_genres'][0]['id'], 1)
        self.assertEqual(response.json()['favorite_genres'][0]['name'], 'Genre 1')

    async def test_delete_user_genre(self):
        response = await self.client_auth.delete(
            path=self.url + 'genres/3'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['favorite_genres']), 1)
        self.assertEqual(response.json()['favorite_genres'][0]['id'], 2)
        self.assertEqual(response.json()['favorite_genres'][0]['name'], 'Genre 2')

    async def test_add_user_author(self):
        response = await self.client_auth.post(
            path=self.url + 'authors/1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['followed_authors'][0]['id'], 1)
        self.assertEqual(response.json()['followed_authors'][0]['name'], 'Author 1')

    async def test_delete_user_author(self):
        response = await self.client_auth.delete(
            path=self.url + 'authors/3'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['followed_authors']), 1)
        self.assertEqual(response.json()['followed_authors'][0]['id'], 2)
        self.assertEqual(response.json()['followed_authors'][0]['name'], 'Author 2')

    async def test_add_user_publisher(self):
        response = await self.client_auth.post(
            path=self.url + 'publishers/1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['followed_publishers'][0]['id'], 1)
        self.assertEqual(response.json()['followed_publishers'][0]['name'], 'Publisher 1')

    async def test_delete_user_publisher(self):
        response = await self.client_auth.delete(
            path=self.url + 'publishers/3'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['followed_publishers']), 1)
        self.assertEqual(response.json()['followed_publishers'][0]['id'], 2)
        self.assertEqual(response.json()['followed_publishers'][0]['name'], 'Publisher 2')

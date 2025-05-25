from django.test import AsyncClient, TestCase

from BookBearApi.models import Author


class TestAuthorController(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/v1/author/'

        cls.author1 = Author.objects.create(
            name='Author 1',
            birth_date='2000-01-01',
        )
        cls.author2 = Author.objects.create(
            name='Author 2',
            birth_date='2000-01-01',
        )
        cls.author3 = Author.objects.create(
            name='Author 3',
            birth_date='2000-01-01',
        )

    async def test_get_authors(self):
        client = AsyncClient()
        response = await client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nb_items'], 3)
        self.assertEqual(response.json()['items'][0]['id'], 1)
        self.assertEqual(response.json()['items'][0]['name'], 'Author 1')
        self.assertEqual(response.json()['items'][1]['id'], 2)
        self.assertEqual(response.json()['items'][1]['name'], 'Author 2')
        self.assertEqual(response.json()['items'][2]['id'], 3)
        self.assertEqual(response.json()['items'][2]['name'], 'Author 3')

    async def test_get_author(self):
        client = AsyncClient()
        response = await client.get(self.url + '1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Author 1')

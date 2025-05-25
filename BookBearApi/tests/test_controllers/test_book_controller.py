from django.test import AsyncClient, TestCase

from BookBearApi.models import Book


class TestBookController(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/v1/book/'

        cls.book1 = Book.objects.create(
            title='Book 1',
            age_rating='E',
            publication_date='2000-01-01',
        )
        cls.book2 = Book.objects.create(
            title='Book 2',
            age_rating='E',
            publication_date='2000-01-01',
        )
        cls.book3 = Book.objects.create(
            title='Book 3',
            age_rating='E',
            publication_date='2000-01-01',
        )

    async def test_get_books(self):
        client = AsyncClient()
        response = await client.get(path=self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nb_items'], 3)
        self.assertEqual(response.json()['items'][0]['id'], 1)
        self.assertEqual(response.json()['items'][0]['title'], 'Book 1')
        self.assertEqual(response.json()['items'][1]['id'], 2)
        self.assertEqual(response.json()['items'][1]['title'], 'Book 2')
        self.assertEqual(response.json()['items'][2]['id'], 3)
        self.assertEqual(response.json()['items'][2]['title'], 'Book 3')

    async def test_get_book(self):
        client = AsyncClient()
        response = await client.get(path=self.url + '1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['title'], 'Book 1')

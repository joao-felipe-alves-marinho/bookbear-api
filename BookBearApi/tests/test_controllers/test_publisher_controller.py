from django.test import AsyncClient, TestCase

from BookBearApi.models import Publisher


class TestPublisherController(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/v1/publisher/'

        cls.publisher1 = Publisher.objects.create(
            name='Publisher 1',
        )
        cls.publisher2 = Publisher.objects.create(
            name='Publisher 2',
        )
        cls.publisher3 = Publisher.objects.create(
            name='Publisher 3',
        )

    async def test_get_publishers(self):
        client = AsyncClient()
        response = await client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nb_items'], 3)
        self.assertEqual(response.json()['items'][0]['id'], 1)
        self.assertEqual(response.json()['items'][0]['name'], 'Publisher 1')
        self.assertEqual(response.json()['items'][1]['id'], 2)
        self.assertEqual(response.json()['items'][1]['name'], 'Publisher 2')
        self.assertEqual(response.json()['items'][2]['id'], 3)
        self.assertEqual(response.json()['items'][2]['name'], 'Publisher 3')

    async def test_get_publisher(self):
        client = AsyncClient()
        response = await client.get(self.url + '1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Publisher 1')

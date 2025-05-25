from django.test import AsyncClient, TestCase

from BookBearApi.models import Genre


class TestGenreController(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/v1/genre/'

        cls.genre1 = Genre.objects.create(
            name='Genre 1',
        )
        cls.genre2 = Genre.objects.create(
            name='Genre 2',
        )
        cls.genre3 = Genre.objects.create(
            name='Genre 3',
        )

    async def test_get_genres(self):
        client = AsyncClient()
        response = await client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nb_items'], 3)
        self.assertEqual(response.json()['items'][0]['id'], 1)
        self.assertEqual(response.json()['items'][0]['name'], 'Genre 1')
        self.assertEqual(response.json()['items'][1]['id'], 2)
        self.assertEqual(response.json()['items'][1]['name'], 'Genre 2')
        self.assertEqual(response.json()['items'][2]['id'], 3)
        self.assertEqual(response.json()['items'][2]['name'], 'Genre 3')

    async def test_get_genre(self):
        client = AsyncClient()
        response = await client.get(self.url + '1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Genre 1')

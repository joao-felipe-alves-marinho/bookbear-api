import json

from asgiref.sync import async_to_sync
from django.test import TestCase, AsyncClient

from BookBearApi.models import User, Author, Publisher, Genre, Book, UserBook


class TestCaseWithData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password='user1',
            birth_date='2000-01-01',
            gender='MC',
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            email='user2@gmail.com',
            password='user2',
            birth_date='2000-01-01',
            gender='FC',
        )

        cls.admin = User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin',
            birth_date='2000-01-01',
            gender='MC'
        )

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

        cls.publisher1 = Publisher.objects.create(
            name='Publisher 1',
        )
        cls.publisher2 = Publisher.objects.create(
            name='Publisher 2',
        )
        cls.publisher3 = Publisher.objects.create(
            name='Publisher 3',
        )

        cls.genre1 = Genre.objects.create(
            name='Genre 1',
        )
        cls.genre2 = Genre.objects.create(
            name='Genre 2',
        )
        cls.genre3 = Genre.objects.create(
            name='Genre 3',
        )

        cls.book1 = Book.objects.create(
            title='Book 1',
            age_rating='E',
            publisher_id=1,
            publication_date='2000-01-01',
        )
        cls.book1.authors.add(cls.author1)
        cls.book1.genres.add(cls.genre1)
        cls.book2 = Book.objects.create(
            title='Book 2',
            age_rating='T',
            publisher_id=2,
            publication_date='2000-01-01',
        )
        cls.book2.authors.add(cls.author2)
        cls.book2.genres.add(cls.genre2)
        cls.book3 = Book.objects.create(
            title='Book 3',
            age_rating='M',
            publisher_id=3,
            publication_date='2000-01-01',
        )

        cls.user_book1 = UserBook.objects.create(
            user=cls.user,
            book=cls.book2,
            situation='C',
            rating=5,
            review='Review of the book',
        )
        cls.user_book2 = UserBook.objects.create(
            user=cls.user,
            book=cls.book3,
            situation='R'
        )

        cls.user.favorite_genres.add(cls.genre2)
        cls.user.favorite_genres.add(cls.genre3)
        cls.user.followed_authors.add(cls.author2)
        cls.user.followed_authors.add(cls.author3)
        cls.user.followed_publishers.add(cls.publisher2)
        cls.user.followed_publishers.add(cls.publisher3)

        cls.access_token = async_to_sync(cls.get_access_token)()

        cls.client_auth = AsyncClient(AUTHORIZATION=f'Bearer {cls.access_token}')

    @classmethod
    async def get_access_token(cls):
        client = AsyncClient()
        response_token = await client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'username': 'user1@gmail.com',
                'password': 'user1'
            }),
            content_type='application/json',
        )
        return response_token.json()['access']

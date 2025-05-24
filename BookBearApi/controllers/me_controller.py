from http import HTTPStatus
from typing import List

from asgiref.sync import sync_to_async
from django.shortcuts import aget_object_or_404
from ninja import File
from ninja.files import UploadedFile
from ninja_extra import (
    api_controller,
    ControllerBase,
    permissions, route
)

from BookBearApi.models import User, Book, UserBook, Genre, Author, Publisher
from BookBearApi.schemas import UserSchema, UpdateUserSchema, UserBookSchema, CreateUserBookSchema, UpdateUserBookSchema


@api_controller('/me', tags=['me'], permissions=[permissions.IsAuthenticated])
class MeController(ControllerBase):
    @route.get('/', response=UserSchema)
    async def me(self):
        """
        Get the current user.
        :return: UserSchema
        """
        return self.context.request.user

    @route.patch('/', response=UserSchema)
    async def update_me(self, payload: UpdateUserSchema):
        """
        Update the current user.
        :param payload: UpdateUserSchema
        :return: UserSchema
        """
        user = self.context.request.user
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(user, attr, value)
        await user.asave()
        return user

    @route.post('/avatar', response=UserSchema)
    async def upload_avatar(self, avatar: File[UploadedFile]):
        user = self.context.request.user
        await sync_to_async(user.avatar.delete)()
        user.avatar = avatar
        await user.asave()
        return user

    @route.delete('/avatar', response=UserSchema)
    async def delete_avatar(self):
        user = self.context.request.user
        await sync_to_async(user.avatar.delete)()
        user.avatar = None
        await user.asave()
        return user

    @route.delete('/', response={204: None})
    async def delete_me(self):
        """
        Delete the current user.
        :return: None
        """
        user = self.context.request.user
        await user.adelete()
        return HTTPStatus.NO_CONTENT, None

    @route.get('/books', response=List[UserBookSchema])
    async def get_user_books(self):
        """
        Get the books of the current user.
        :return: List[BookRelationshipSchema]
        """
        user = await aget_object_or_404(User, id=self.context.request.user.id)
        return [user_book async for user_book in user.reviewed_books.all()]

    @route.post('/books/{int:book_id}', response=UserBookSchema)
    async def add_user_book(self, book_id: int, payload: CreateUserBookSchema):
        """
        Add a book to the current user.
        :param book_id: int
        :param payload: CreateUserBookSchema
        :return: UserBookSchema
        """
        user = self.context.request.user
        book = await aget_object_or_404(Book, id=book_id)
        user_book = await UserBook.objects.acreate(user=user, book=book, **payload.dict(exclude_unset=True))
        return user_book

    @route.patch('/books/{int:book_id}', response=UserBookSchema)
    async def update_user_book(self, book_id: int, payload: UpdateUserBookSchema):
        """
        Update a book of the current user.
        :param book_id: int
        :param payload: UpdateUserBookSchema
        :return: UserBookSchema
        """
        user = self.context.request.user
        user_book = await aget_object_or_404(UserBook, user=user, book__id=book_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(user_book, attr, value)
        await user_book.asave()
        return user_book

    @route.delete('/books/{int:book_id}', response={204: None})
    async def delete_user_book(self, book_id: int):
        """
        Delete a book of the current user.
        :param book_id: int
        :return: None
        """
        user = self.context.request.user
        user_book = await aget_object_or_404(UserBook, user=user, book__id=book_id)
        await user_book.adelete()
        return HTTPStatus.NO_CONTENT, None

    @route.post('/genres/{int:genre_id}', response=UserSchema)
    async def add_user_genre(self, genre_id: int):
        """
        Add a favorite genre to the current user.
        :param genre_id: int
        :return: UserSchema
        """
        user = self.context.request.user
        genre = await aget_object_or_404(Genre, id=genre_id)
        await genre.users.aadd(user)
        return user

    @route.delete('/genres/{int:genre_id}', response=UserSchema)
    async def remove_user_genre(self, genre_id: int):
        """
        Remove a favorite genre from the current user.
        :param genre_id: int
        :return: UserSchema
        """
        user = self.context.request.user
        genre = await aget_object_or_404(Genre, id=genre_id)
        await genre.users.aremove(user)
        return user

    @route.post('/authors/{int:author_id}', response=UserSchema)
    async def add_user_author(self, author_id: int):
        """
        Follow an author.
        :param author_id: int
        :return: UserSchema
        """
        user = self.context.request.user
        author = await aget_object_or_404(Author, id=author_id)
        await author.followers.aadd(user)
        return user

    @route.delete('/authors/{int:author_id}', response=UserSchema)
    async def remove_user_author(self, author_id: int):
        """
        Unfollow an author.
        :param author_id: int
        :return: UserSchema
        """
        user = self.context.request.user
        author = await aget_object_or_404(Author, id=author_id)
        await author.followers.aremove(user)
        return user

    @route.post('/publishers/{int:publisher_id}', response=UserSchema)
    async def add_user_publisher(self, publisher_id: int):
        """
        Follow a publisher.
        :param publisher_id: int
        :return: UserSchema
        """
        user = self.context.request.user
        publisher = await aget_object_or_404(Publisher, id=publisher_id)
        await publisher.followers.aadd(user)
        return user

    @route.delete('/publishers/{int:publisher_id}', response=UserSchema)
    async def remove_user_publisher(self, publisher_id: int):
        """
        Unfollow a publisher.
        :param publisher_id: int
        :return: UserSchema
        """
        user = self.context.request.user
        publisher = await aget_object_or_404(Publisher, id=publisher_id)
        await publisher.followers.aremove(user)
        return user

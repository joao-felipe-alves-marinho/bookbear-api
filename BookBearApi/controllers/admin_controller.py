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
from BookBearApi.schemas import UserSchema, UpdateUserSchema, BookRelationshipSchema, UserBookSchema, \
    CreateUserBookSchema, UpdateUserBookSchema, BookSchema, CreateBookSchema, AuthorSchema, CreateAuthorSchema, \
    PublisherSchema, GenreSchema, CreateGenreSchema, UpdateBookSchema, UpdateAuthorSchema


@api_controller('/admin', tags=['admin'], permissions=[permissions.IsAdminUser])
class AdminController(ControllerBase):
    @route.post('/book', response={201: BookSchema})
    async def create_book(self, payload: CreateBookSchema, cover: File[UploadedFile] = None):
        """
        Create a book.
        :param payload: CreateBookSchema
        :param cover: File[UploadedFile]
        :return: BookSchema
        """
        book = await Book.objects.acreate(cover=cover, **payload.dict(exclude_unset=True))
        return HTTPStatus.CREATED, book

    @route.patch('/book/{book_id}', response=BookSchema)
    async def update_book(self, book_id: int, payload: UpdateBookSchema):
        """
        Update a book.
        :param book_id: int
        :param payload: UpdateBookSchema
        :return: BookSchema
        """
        book = await aget_object_or_404(Book, id=book_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(book, attr, value)
        await book.asave()
        return book

    @route.post('/book/{book_id}', response=BookSchema)
    async def upload_cover(self, book_id: int, cover: File[UploadedFile]):
        """
        Upload a cover for a book.
        :param book_id: int
        :param cover: File[UploadedFile]
        :return: BookSchema
        """
        book = await aget_object_or_404(Book, id=book_id)
        await sync_to_async(book.cover.delete)()
        book.cover = cover
        await book.asave()
        return book

    @route.delete('/book/{book_id}/cover', response=BookSchema)
    async def delete_cover(self, book_id: int):
        """
        Delete a cover for a book.
        :param book_id: int
        :return: BookSchema
        """
        book = await aget_object_or_404(Book, id=book_id)
        await sync_to_async(book.cover.delete)()
        book.cover = None
        await book.asave()
        return book

    @route.delete('/book/{book_id}', response={204: None})
    async def delete_book(self, book_id: int):
        """
        Delete a book.
        :param book_id: int
        :return: BookSchema
        """
        book = await aget_object_or_404(Book, id=book_id)
        await sync_to_async(book.cover.delete)()
        await book.adelete()
        return HTTPStatus.NO_CONTENT, None

    @route.post('/author', response={201: AuthorSchema})
    async def create_author(self, payload: CreateAuthorSchema, avatar: File[UploadedFile] = None):
        """
        Create an author.
        :param payload: CreateAuthorSchema
        :param avatar: File[UploadedFile]
        :return: AuthorSchema
        """
        author = await Author.objects.acreate(avatar=avatar, **payload.dict(exclude_unset=True))
        return HTTPStatus.CREATED, author

    @route.patch('/author/{author_id}', response=AuthorSchema)
    async def update_author(self, author_id: int, payload: UpdateAuthorSchema):
        """
        Update an author.
        :param author_id: int
        :param payload: UpdateAuthorSchema
        :return: AuthorSchema
        """
        author = await aget_object_or_404(Author, id=author_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(author, attr, value)
        await author.asave()
        return author

    @route.post('/author/{author_id}', response=AuthorSchema)
    async def upload_avatar(self, author_id: int, avatar: File[UploadedFile]):
        """
        Upload an avatar for an author.
        :param author_id: int
        :param avatar: File[UploadedFile]
        :return: AuthorSchema
        """
        author = await aget_object_or_404(Author, id=author_id)
        await sync_to_async(author.avatar.delete)()
        author.avatar = avatar
        await author.asave()
        return author

    @route.delete('/author/{author_id}/avatar', response=AuthorSchema)
    async def delete_avatar(self, author_id: int):
        """
        Delete an avatar for an author.
        :param author_id: int
        :return: AuthorSchema
        """
        author = await aget_object_or_404(Author, id=author_id)
        await sync_to_async(author.avatar.delete)()
        author.avatar = None
        await author.asave()
        return author

    @route.delete('/author/{author_id}', response={204: None})
    async def delete_author(self, author_id: int):
        """
        Delete an author.
        :param author_id: int
        :return: AuthorSchema
        """
        author = await aget_object_or_404(Author, id=author_id)
        await sync_to_async(author.avatar.delete)()
        await author.adelete()
        return HTTPStatus.NO_CONTENT, None

    @route.post('/publisher', response={201: PublisherSchema})
    async def create_publisher(self, payload: PublisherSchema, logo: File[UploadedFile] = None):
        """
        Create a publisher.
        :param payload: PublisherSchema
        :param logo: File[UploadedFile]
        :return: PublisherSchema
        """
        publisher = await Publisher.objects.acreate(logo=logo, **payload.dict(exclude_unset=True))
        return HTTPStatus.CREATED, publisher

    @route.post('/genre', response={201: GenreSchema})
    async def create_genre(self, payload: CreateGenreSchema):
        """
        Create a genre.
        :param payload: GenreSchema
        :return: GenreSchema
        """
        genre = await Genre.objects.acreate(**payload.dict(exclude_unset=True))
        return HTTPStatus.CREATED, genre

    @route.patch('/genre/{genre_id}', response=GenreSchema)
    async def update_genre(self, genre_id: int, payload: CreateGenreSchema):
        """
        Update a genre.
        :param genre_id: int
        :param payload: CreateGenreSchema
        :return: GenreSchema
        """
        genre = await aget_object_or_404(Genre, id=genre_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(genre, attr, value)
        await genre.asave()
        return genre

    @route.delete('/genre/{genre_id}', response={204: None})
    async def delete_genre(self, genre_id: int):
        """
        Delete a genre.
        :param genre_id: int
        :return: GenreSchema
        """
        genre = await aget_object_or_404(Genre, id=genre_id)
        await genre.adelete()
        return HTTPStatus.NO_CONTENT, None




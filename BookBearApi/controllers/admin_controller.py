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

from BookBearApi.models import Book, Genre, Author, Publisher
from BookBearApi.schemas import BookSchema, CreateBookSchema, AuthorSchema, CreateAuthorSchema, \
    PublisherSchema, GenreSchema, CreateGenreSchema, UpdateBookSchema, UpdateAuthorSchema, CreatePublisherSchema, \
    UpdatePublisherSchema


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
        publisher = await aget_object_or_404(Publisher, id=payload.publisher)
        book = await Book.objects.acreate(cover=cover,
                                          publisher=publisher,
                                          **payload.dict(exclude_unset=True,
                                                         exclude={'authors', 'genres', 'publisher'}))
        if payload.authors:
            authors = [author async for author in Author.objects.filter(id__in=payload.authors).all()]
            await book.authors.aadd(*authors)
        if payload.genres:
            genres = [genre async for genre in Genre.objects.filter(id__in=payload.genres).all()]
            await book.genres.aadd(*genres)
        return HTTPStatus.CREATED, book

    @route.patch('/book/{int:book_id}', response=BookSchema)
    async def update_book(self, book_id: int, payload: UpdateBookSchema):
        """
        Update a book.
        :param book_id: int
        :param payload: UpdateBookSchema
        :return: BookSchema
        """
        book = await aget_object_or_404(Book, id=book_id)
        for attr, value in payload.dict(exclude_unset=True, exclude={'authors', 'genres', 'publisher'}).items():
            setattr(book, attr, value)
        if payload.publisher:
            publisher = await aget_object_or_404(Publisher, id=payload.publisher)
            book.publisher = publisher
        if payload.authors:
            authors = [author async for author in Author.objects.filter(id__in=payload.authors).all()]
            await book.authors.aremove(
                *[author async for author in book.authors.all() if author.id not in payload.authors]
            )
            await book.authors.aadd(*authors)
        if payload.genres:
            genres = [genre async for genre in Genre.objects.filter(id__in=payload.genres).all()]
            await book.genres.aremove(
                *[genre async for genre in book.genres.all() if genre.id not in payload.genres]
            )
            await book.genres.aadd(*genres)
        await book.asave()
        return book

    @route.post('/book/{int:book_id}', response=BookSchema)
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

    @route.delete('/book/{int:book_id}/cover', response=BookSchema)
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

    @route.delete('/book/{int:book_id}', response={204: None})
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

    @route.patch('/author/{int:author_id}', response=AuthorSchema)
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

    @route.post('/author/{int:author_id}', response=AuthorSchema)
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

    @route.delete('/author/{int:author_id}/avatar', response=AuthorSchema)
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

    @route.delete('/author/{int:author_id}', response={204: None})
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

    @route.get('/publisher', response=List[PublisherSchema])
    async def list_publishers(self):
        """
        List all publishers.
        :return: List[PublisherSchema]
        """
        return [publisher async for publisher in Publisher.objects.all()]

    @route.post('/publisher', response={201: PublisherSchema})
    async def create_publisher(self, payload: CreatePublisherSchema, logo: File[UploadedFile] = None):
        """
        Create a publisher.
        :param payload: CreatePublisherSchema
        :param logo: File[UploadedFile]
        :return: PublisherSchema
        """
        publisher = await Publisher.objects.acreate(logo=logo, **payload.dict(exclude_unset=True))
        return HTTPStatus.CREATED, publisher

    @route.patch('/publisher/{int:publisher_id}', response=PublisherSchema)
    async def update_publisher(self, publisher_id: int, payload: UpdatePublisherSchema):
        """
        Update a publisher.
        :param publisher_id: int
        :param payload: UpdatePublisherSchema
        :return: PublisherSchema
        """
        publisher = await aget_object_or_404(Publisher, id=publisher_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(publisher, attr, value)
        await publisher.asave()
        return publisher

    @route.post('/publisher/{int:publisher_id}/logo', response=PublisherSchema)
    async def upload_logo(self, publisher_id: int, logo: File[UploadedFile]):
        """
        Upload a logo for a publisher.
        :param publisher_id: int
        :param logo: File[UploadedFile]
        :return: PublisherSchema
        """
        publisher = await aget_object_or_404(Publisher, id=publisher_id)
        await sync_to_async(publisher.logo.delete)()
        publisher.logo = logo
        await publisher.asave()
        return publisher

    @route.delete('/publisher/{int:publisher_id}/logo', response=PublisherSchema)
    async def delete_logo(self, publisher_id: int):
        """
        Delete a logo for a publisher.
        :param publisher_id: int
        :return: PublisherSchema
        """
        publisher = await aget_object_or_404(Publisher, id=publisher_id)
        await sync_to_async(publisher.logo.delete)()
        publisher.logo = None
        await publisher.asave()
        return publisher

    @route.delete('/publisher/{int:publisher_id}', response={204: None})
    async def delete_publisher(self, publisher_id: int):
        """
        Delete a publisher.
        :param publisher_id: int
        :return: PublisherSchema
        """
        publisher = await aget_object_or_404(Publisher, id=publisher_id)
        await sync_to_async(publisher.logo.delete)()
        await publisher.adelete()
        return HTTPStatus.NO_CONTENT, None

    @route.post('/genre', response={201: GenreSchema})
    async def create_genre(self, payload: CreateGenreSchema):
        """
        Create a genre.
        :param payload: GenreSchema
        :return: GenreSchema
        """
        genre = await Genre.objects.acreate(**payload.dict(exclude_unset=True))
        return HTTPStatus.CREATED, genre

    @route.patch('/genre/{int:genre_id}', response=GenreSchema)
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

    @route.delete('/genre/{int:genre_id}', response={204: None})
    async def delete_genre(self, genre_id: int):
        """
        Delete a genre.
        :param genre_id: int
        :return: GenreSchema
        """
        genre = await aget_object_or_404(Genre, id=genre_id)
        await genre.adelete()
        return HTTPStatus.NO_CONTENT, None

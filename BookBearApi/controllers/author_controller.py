from typing import List

from django.shortcuts import aget_object_or_404
from ninja_extra.ordering import ordering, Ordering
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)

from BookBearApi.models import Book
from BookBearApi.schemas import BookSchema, AuthorSchema


@api_controller('/author', tags=['author'], permissions=[permissions.AllowAny], auth=None)
class AuthorController(ControllerBase):
    @route.get('/', response=List[AuthorSchema])
    async def list_books(self):
        """
        List all authors.
        :return: List[BookSchema]
        """
        return [book async for book in Book.objects.all()]

    @route.get('/{book_id}', response=BookSchema)
    async def get_book(self, book_id: int):
        """
        Get a book by id.
        :param book_id: int
        :return: BookSchema
        """
        return await aget_object_or_404(Book, id=book_id)

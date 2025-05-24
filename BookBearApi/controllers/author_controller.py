from typing import List

from django.shortcuts import aget_object_or_404
from ninja import Query
from ninja.pagination import paginate
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)

from BookBearApi.models import Author
from BookBearApi.schemas import AuthorSchema, FilterAuthorSchema, AsyncPageNumberPagination


@api_controller('/author', tags=['author'], permissions=[permissions.AllowAny], auth=None)
class AuthorController(ControllerBase):
    @route.get('/', response=List[AuthorSchema])
    @paginate(AsyncPageNumberPagination)
    async def get_authors(self, filters: FilterAuthorSchema = Query(...)):
        """
        Get a list of authors.
        :return: List[AuthorSchema]
        """
        return [author async for author in filters.filter(Author.objects.all())]

    @route.get('/{int:author_id}', response=AuthorSchema)
    async def get_book(self, author_id: int):
        """
        Get an author by id.
        :param author_id: int
        :return: AuthorSchema
        """
        return await aget_object_or_404(Author, id=author_id)

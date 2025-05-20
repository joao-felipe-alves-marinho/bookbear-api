from typing import List

from django.shortcuts import aget_object_or_404
from ninja import Query
from ninja.pagination import paginate
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)

from BookBearApi.models import Genre
from BookBearApi.schemas import GenreSchema, FilterGenreSchema
from BookBearApi.schemas.pagination_schema import AsyncPageNumberPagination


@api_controller('/genre', tags=['genre'], permissions=[permissions.AllowAny], auth=None)
class GenreController(ControllerBase):
    @route.get('/', response=List[GenreSchema])
    @paginate(AsyncPageNumberPagination)
    async def get_genres(self, filters: FilterGenreSchema = Query(...)):
        """
        Get a list of all genres.
        :return: List[GenreSchema]
        """
        return [genre async for genre in filters.filter(Genre.objects.all())]

    @route.get('/{genre_id}', response=GenreSchema)
    async def get_genre(self, genre_id: int):
        """
        Get a genre by id.
        :param genre_id: int
        :return: GenreSchema
        """
        return await aget_object_or_404(Genre, id=genre_id)

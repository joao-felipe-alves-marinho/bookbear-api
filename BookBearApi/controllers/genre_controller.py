from typing import List

from django.shortcuts import aget_object_or_404
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)

from BookBearApi.models import Genre
from BookBearApi.schemas import GenreSchema


@api_controller('/genre', tags=['genre'], permissions=[permissions.AllowAny], auth=None)
class GenreController(ControllerBase):
    @route.get('/', response=List[GenreSchema])
    async def get_genres(self):
        """
        Get a list of all genres.
        :return: List[GenreSchema]
        """
        return [genre async for genre in Genre.objects.all()]

    @route.get('/{genre_id}', response=GenreSchema)
    async def get_genre(self, genre_id: int):
        """
        Get a genre by id.
        :param genre_id: int
        :return: GenreSchema
        """
        return await aget_object_or_404(Genre, id=genre_id)

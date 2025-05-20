from typing import List, Optional

from ninja import FilterSchema
from ninja_schema import ModelSchema
from pydantic import Field

from BookBearApi.models import Genre
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueNameMixin


class GenreSchema(ModelSchema):
    books: List['BookRelationshipSchema'] = None

    class Config:
        model = Genre
        include = ['id', 'name']


class CreateGenreSchema(ModelSchema, UniqueNameMixin):
    class Config:
        model = Genre


class UpdateGenreSchema(ModelSchema):
    class Config:
        model = Genre
        include = ['name']
        optional = ['name']


class FilterGenreSchema(FilterSchema):
    name: Optional[str] = Field(
        None, description='Filter by genres name',
        q='genre__name__icontains'
    )

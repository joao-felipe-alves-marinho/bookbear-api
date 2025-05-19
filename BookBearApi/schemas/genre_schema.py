from typing import List

from ninja_schema import ModelSchema

from BookBearApi.models import Genre
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema, UserRelationshipSchema
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

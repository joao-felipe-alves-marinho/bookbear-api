from typing import Optional, List

from ninja import FilterSchema
from ninja_schema import ModelSchema
from pydantic import Field

from BookBearApi.models import Author
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueNameMixin


class AuthorSchema(ModelSchema):
    avatar: Optional[str] = None
    books: List['BookRelationshipSchema'] = None

    class Config:
        model = Author
        include = ['id', 'name', 'birth_date']


class CreateAuthorSchema(ModelSchema, UniqueNameMixin):
    class Config:
        model = Author
        include = ['name', 'birth_date']


class UpdateAuthorSchema(ModelSchema):
    class Config:
        model = Author
        include = ['name', 'birth_date']
        optional = '__all__'


class FilterAuthorSchema(FilterSchema):
    name: Optional[str] = Field(
        None, description='Filter by authors name',
        q='author__name__icontains'
    )

from typing import Optional, List

from ninja_schema import ModelSchema

from BookBearApi.models import Author
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema, UserRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueNameMixin


class AuthorSchema(ModelSchema):
    avatar: Optional[str] = None
    books: List['BookRelationshipSchema'] = None
    followers: List['UserRelationshipSchema'] = None

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

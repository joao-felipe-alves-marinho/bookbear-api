from typing import Optional, List

from ninja import FilterSchema, ModelSchema
from pydantic import Field

from BookBearApi.models import Author
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueNameMixin


class AuthorSchema(ModelSchema):
    avatar: Optional[str] = None
    books: List['BookRelationshipSchema'] = None

    class Meta:
        model = Author
        fields = ('id', 'name', 'birth_date')


class CreateAuthorSchema(ModelSchema, UniqueNameMixin):
    class Meta:
        model = Author
        fields = ('name', 'birth_date')


class UpdateAuthorSchema(ModelSchema):
    class Meta:
        model = Author
        fields = ('name', 'birth_date')
        fields_optional = '__all__'


class FilterAuthorSchema(FilterSchema):
    name: Optional[str] = Field(
        None, description='Filter by authors name',
        q='name__icontains'
    )

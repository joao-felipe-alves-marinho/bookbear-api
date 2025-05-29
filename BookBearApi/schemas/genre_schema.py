from typing import List, Optional

from ninja import FilterSchema, ModelSchema
from pydantic import Field

from BookBearApi.models import Genre
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueNameMixin


class GenreSchema(ModelSchema):
    books: List['BookRelationshipSchema'] = None

    class Meta:
        model = Genre
        fields = ('id', 'name')


class CreateGenreSchema(ModelSchema, UniqueNameMixin):
    class Meta:
        model = Genre
        fields = ('name',)


class UpdateGenreSchema(ModelSchema):
    class Meta:
        model = Genre
        fields = ('name',)
        fields_optional = 'name'


class FilterGenreSchema(FilterSchema):
    name: Optional[str] = Field(
        None, description='Filter by genres name',
        q='name__icontains'
    )

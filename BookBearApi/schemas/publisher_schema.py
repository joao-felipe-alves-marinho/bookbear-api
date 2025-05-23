from typing import Optional, List

from ninja import FilterSchema, ModelSchema
from pydantic import Field

from BookBearApi.models import Publisher
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueNameMixin


class PublisherSchema(ModelSchema):
    logo: Optional[str] = None
    books: List['BookRelationshipSchema'] = None

    class Meta:
        model = Publisher
        fields = ('id', 'name')


class CreatePublisherSchema(ModelSchema, UniqueNameMixin):
    class Meta:
        model = Publisher
        fields = ('name',)


class UpdatePublisherSchema(ModelSchema):
    class Meta:
        model = Publisher
        fields = ('name',)
        fields_optional = 'name'


class FilterPublisherSchema(FilterSchema):
    name: Optional[str] = Field(
        None, description='Filter by publishers name',
        q='publisher__name__icontains'
    )

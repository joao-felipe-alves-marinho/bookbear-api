from typing import Optional, List

from ninja_schema import ModelSchema

from BookBearApi.models import Publisher
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema, UserRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueNameMixin


class PublisherSchema(ModelSchema):
    logo: Optional[str] = None
    books: List['BookRelationshipSchema'] = None

    class Config:
        model = Publisher
        include = ['id', 'name']


class CreatePublisherSchema(ModelSchema, UniqueNameMixin):
    class Config:
        model = Publisher
        include = ['name']


class UpdatePublisherSchema(ModelSchema):
    class Config:
        model = Publisher
        include = ['name']
        optional = ['name']

from typing import Optional, List, Any, Type, cast, Dict

from ninja_schema import ModelSchema, model_validator

from BookBearApi.models import User, UserBook
from BookBearApi.schemas.author_schema import AuthorSchema
from BookBearApi.schemas.genre_schema import GenreSchema
from BookBearApi.schemas.publisher_schema import PublisherSchema
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema, UserRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueEmailMixin


class UserSchema(ModelSchema):
    reviewed_books: List['UserBookSchema'] = None
    followed_authors: List[AuthorSchema] = None
    followed_publishers: List[PublisherSchema] = None
    favorite_genres: List[GenreSchema] = None

    avatar: Optional[str] = None

    class Config:
        model = User
        include = ['id', 'username', 'email', 'birth_date', 'gender', 'summary']


class CreateUserSchema(ModelSchema, UniqueEmailMixin):
    class Config:
        model = User
        include = ['username', 'email', 'password', 'birth_date', 'gender', 'summary']


class UpdateUserSchema(ModelSchema, UniqueEmailMixin):
    class Config:
        model = User
        include = ['username', 'email', 'birth_date', 'gender', 'summary']
        optional = '__all__'


class UserBookSchema(ModelSchema):
    book: BookRelationshipSchema

    class Config:
        model = UserBook
        include = ['situation', 'rating', 'review']


class CreateUserBookSchema(ModelSchema):
    class Config:
        model = UserBook
        include = ['situation', 'rating', 'review']
        optional = ['rating', 'review']


class UpdateUserBookSchema(CreateUserBookSchema):
    class Config(CreateUserBookSchema.Config):
        optional = '__all__'


class ReviewBookSchema(ModelSchema):
    user: UserRelationshipSchema

    class Config:
        model = UserBook
        include = ['situation', 'rating', 'review']

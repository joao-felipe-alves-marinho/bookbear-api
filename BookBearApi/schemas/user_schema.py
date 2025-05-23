from typing import Optional, List

from ninja import ModelSchema

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

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'birth_date', 'gender', 'summary')


class CreateUserSchema(ModelSchema, UniqueEmailMixin):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'birth_date', 'gender', 'summary')
        fields_optional = ['summary']


class UpdateUserSchema(ModelSchema, UniqueEmailMixin):
    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'gender', 'summary')
        fields_optional = '__all__'


class UserBookSchema(ModelSchema):
    book: BookRelationshipSchema

    class Meta:
        model = UserBook
        fields = ('situation', 'rating', 'review')


class CreateUserBookSchema(ModelSchema):
    class Meta:
        model = UserBook
        fields = ('situation', 'rating', 'review')
        fields_optional  = ['rating', 'review']


class UpdateUserBookSchema(ModelSchema):
    class Meta:
        model = UserBook
        fields = ('situation', 'rating', 'review')
        fields_optional  = '__all__'


class ReviewBookSchema(ModelSchema):
    user: UserRelationshipSchema

    class Meta:
        model = UserBook
        fields = ('situation', 'rating', 'review')

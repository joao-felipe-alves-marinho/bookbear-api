from typing import Optional, List

from ninja import ModelSchema, FilterSchema
from pydantic import Field

from BookBearApi.models import User, UserBook
from BookBearApi.schemas.relationship_schema import BookRelationshipSchema, UserRelationshipSchema, \
    AuthorRelationshipSchema, PublisherRelationshipSchema, GenreRelationshipSchema
from BookBearApi.schemas.validators_mixin import UniqueEmailMixin


class UserSchema(ModelSchema):
    reviewed_books: List['UserBookSchema'] = None
    followed_authors: List[AuthorRelationshipSchema] = None
    followed_publishers: List[PublisherRelationshipSchema] = None
    favorite_genres: List[GenreRelationshipSchema] = None

    avatar: Optional[str] = None

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'birth_date', 'gender', 'summary', 'is_superuser')


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
        fields_optional = ['rating', 'review']


class UpdateUserBookSchema(ModelSchema):
    class Meta:
        model = UserBook
        fields = ('situation', 'rating', 'review')
        fields_optional = '__all__'


class ReviewBookSchema(ModelSchema):
    user: UserRelationshipSchema

    class Meta:
        model = UserBook
        fields = ('situation', 'rating', 'review')


class FilterUserSchema(FilterSchema):
    username: Optional[str] = Field(
        None, description='Filter by user name',
        q='user__username__icontains'
    )

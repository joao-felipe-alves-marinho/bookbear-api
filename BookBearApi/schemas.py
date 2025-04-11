from typing import Optional, List, Any, Type, cast, Dict

from django.core.validators import validate_email
from ninja_schema import ModelSchema, model_validator

from django.db.models import QuerySet
from dj_ninja_auth.jwt import app_settings
from dj_ninja_auth.jwt.tokens import RefreshToken
from dj_ninja_auth.jwt.schema import JWTTokenInputSchemaMixin
from dj_ninja_auth.schema import SuccessMessageMixin, LoginInputSchema
from django.contrib.auth.models import update_last_login, AbstractUser
from ninja import Field, Schema
from ninja.pagination import AsyncPaginationBase

from BookBearApi.models import Author, Publisher, Genre, Book, User, UserBook


class UniqueNameMixin:
    class Config:
        model: Any

    @classmethod
    @model_validator('name')
    def validate_unique_name(cls, value: str) -> str:
        model = cls.Config.model
        if model.objects.filter(name=value).exists():
            raise ValueError(f'{model.__name__} with name "{value}" already exists')
        return value


# ---------------------------------------------------------------

class AuthorSchema(ModelSchema):
    avatar: str = None
    books: List['BookRelationshipSchema'] = None
    followers: List['UserRelationshipSchema'] = None

    class Config:
        model = Author
        include = ['id', 'name', 'birth_date']


class CreateAuthorSchema(ModelSchema, UniqueNameMixin):
    class Config:
        model = Author
        include = ['name', 'birth_date']


class UpdateAuthorSchema(CreateAuthorSchema):
    class Config(CreateAuthorSchema.Config):
        optional = '__all__'


# ---------------------------------------------------------------

class PublisherSchema(ModelSchema):
    logo: str = None
    books: List['BookRelationshipSchema'] = None
    followers: List['UserRelationshipSchema'] = None

    class Config:
        model = Publisher
        include = ['id', 'name']


class CreatePublisherSchema(ModelSchema, UniqueNameMixin):
    class Config:
        model = Publisher
        include = ['name']


class UpdatePublisherSchema(CreatePublisherSchema):
    class Config(CreatePublisherSchema.Config):
        optional = '__all__'


# ---------------------------------------------------------------

class GenreSchema(ModelSchema):
    books: List['BookRelationshipSchema'] = None
    users: List['UserRelationshipSchema'] = None

    class Config:
        model = Genre
        include = ['id', 'name']


class CreateGenreSchema(ModelSchema, UniqueNameMixin):
    class Config:
        model = Genre


class UpdateGenreSchema(CreateGenreSchema):
    class Config(CreateGenreSchema.Config):
        optional = '__all__'


# ---------------------------------------------------------------

class BookSchema(ModelSchema):
    authors: List[AuthorSchema] = None
    genres: List[GenreSchema] = None
    publisher: PublisherSchema = None
    reviews: List['ReviewBookSchema'] = None

    cover: str = None

    class Config:
        model = Book
        include = ['id', 'title', 'publication_date', 'synopsis', 'score', 'age_rating', 'publisher', 'authors',
                   'genres']


class CreateBookSchema(ModelSchema):
    class Config:
        model = Book
        include = ['title', 'publication_date', 'synopsis', 'age_rating', 'publisher', 'authors', 'genres']
        optional = ['synopsis', 'publisher', 'authors', 'genres']


class UpdateBookSchema(CreateBookSchema):
    class Config(CreateBookSchema.Config):
        optional = '__all__'


# ---------------------------------------------------------------

class UserSchema(ModelSchema):
    reviewed_books: List['UserBookSchema'] = None
    followed_authors: List[AuthorSchema] = None
    followed_publishers: List[PublisherSchema] = None
    favorite_genres: List[GenreSchema] = None

    avatar: str = None

    class Config:
        model = User
        include = ['id', 'username', 'email', 'birth_date', 'gender', 'summary']


class CreateUserSchema(ModelSchema):
    class Config:
        model = User
        include = ['username', 'email', 'password', 'birth_date', 'gender', 'summary']

    @classmethod
    @model_validator('email')
    def validate_email(cls, value):
        if User.objects.filter(email=value).exists():
            raise ValueError('Email already exists')
        validate_email(value)
        return value


class UpdateUserSchema(CreateUserSchema):
    class Config(CreateUserSchema.Config):
        optional = '__all__'

    @classmethod
    @model_validator('email')
    def validate_email(cls, value):
        if User.objects.filter(email=value).exclude(id=cls.instance.id).exists():
            raise ValueError('Email already exists')
        validate_email(value)
        return value


# ---------------------------------------------------------------

class UserRelationshipSchema(ModelSchema):
    class Config:
        model = User
        include = ['id', 'username']


class AuthorRelationshipSchema(ModelSchema):
    class Config:
        model = Author
        include = ['id', 'name']


class PublisherRelationshipSchema(ModelSchema):
    class Config:
        model = Publisher
        include = ['id', 'name']


class BookRelationshipSchema(ModelSchema):
    publisher: PublisherRelationshipSchema = None
    authors: List[AuthorRelationshipSchema] = None

    class Config:
        model = Book
        include = ['id', 'title', 'score', 'age_rating']


# ---------------------------------------------------------------

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


# ---------------------------------------------------------------

class ReviewBookSchema(ModelSchema):
    user: UserRelationshipSchema

    class Config:
        model = UserBook
        include = ['situation', 'rating', 'review']


# ---------------------------------------------------------------
class TokenRefreshOutputCookieSchema(Schema):
    access: str


class AsyncPageNumberPagination(AsyncPaginationBase):
    def paginate_queryset(self, queryset: QuerySet, pagination: Any, **params: Any) -> Any:
        pass

    class Input(Schema):
        page: int = Field(1, ge=1)
        page_size: int = Field(10, ge=1, le=50)

    class Output(Schema):
        nb_items: int = Field(ge=0)
        nb_pages: int = Field(ge=0)
        page_size: int = Field(ge=1)
        page: int = Field(ge=1)

    async def apaginate_queryset(self, queryset, pagination: Input, **params) -> Any:
        offset = (pagination.page - 1) * pagination.page_size
        nb_items = await self._aitems_count(queryset)

        return {
            "nb_items": nb_items,
            "nb_pages": (nb_items + pagination.page_size - 1) // pagination.page_size,
            "page_size": pagination.page_size,
            "page": pagination.page,
            "items": queryset[offset: offset + pagination.page_size],
        }


class CustomLoginInputSchema(LoginInputSchema):
    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return CustomLoginOutputSchema


class CustomLoginOutputSchema(SuccessMessageMixin):
    user: UserSchema


class CustomTokenInputSchemaBase(JWTTokenInputSchemaMixin, CustomLoginInputSchema):
    _access: Optional[str]
    _refresh: Optional[str]

    def post_validate_schema(self):
        """
        This is a post validate process which is common for any token generating schema.
        :return:
        """
        # get_token can return values that wants to apply to `OutputSchema`

        data = self.get_token(self._user)

        if not isinstance(data, dict):
            raise Exception("`get_token` must return a `typing.Dict` type.")

        if app_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self._user)  # noqa

        self._access = data["access"]
        self._refresh = data["refresh"]

    @classmethod
    def get_response_schema(cls) -> type[Schema]:
        return CustomTokenPairOutputSchema


class CustomTokenPairOutputSchema(CustomLoginOutputSchema):
    access: str
    refresh: str


class CustomTokenPairInputSchema(CustomTokenInputSchemaBase):
    @classmethod
    def get_token(cls, user: AbstractUser) -> Dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        refresh = cast(RefreshToken, refresh)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        return values

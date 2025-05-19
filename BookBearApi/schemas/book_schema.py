from typing import Optional, List

from ninja_schema import ModelSchema

from BookBearApi.models import Book
from BookBearApi.schemas.user_schema import ReviewBookSchema
from BookBearApi.schemas.publisher_schema import PublisherSchema
from BookBearApi.schemas.genre_schema import GenreSchema
from BookBearApi.schemas.author_schema import AuthorSchema


class BookSchema(ModelSchema):
    authors: List[AuthorSchema] = None
    genres: List[GenreSchema] = None
    publisher: Optional[PublisherSchema] = None
    reviews: List['ReviewBookSchema'] = None

    cover: Optional[str] = None

    class Config:
        model = Book
        include = ['id', 'title', 'publication_date', 'synopsis', 'score', 'age_rating', 'publisher', 'authors',
                   'genres']
        use_enum_values = True


class CreateBookSchema(ModelSchema):
    class Config:
        model = Book
        include = ['title', 'publication_date', 'synopsis', 'age_rating', 'publisher', 'authors', 'genres']
        optional = ['synopsis', 'publisher', 'authors', 'genres']


class UpdateBookSchema(ModelSchema):
    class Config:
        model = Book
        include = ['title', 'publication_date', 'synopsis', 'age_rating', 'publisher', 'authors', 'genres']
        optional = '__all__'

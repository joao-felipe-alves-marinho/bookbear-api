from typing import Optional, List

from ninja import FilterSchema
from ninja_schema import ModelSchema
from pydantic import Field

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


class FilterBookSchema(FilterSchema):
    title: Optional[str] = Field(
        None, description='Filter books by title',
        q='title__icontains'
    )

    publication_date: Optional[str] = Field(
        None, description='Filter books by publication date',
        q='publication_date__icontains'
    )

    score: Optional[float] = Field(
        None, description='Filter books by score',
        q='score__icontains'
    )

    age_rating: Optional[str] = Field(
        None, description='Filter books by age rating',
        q='age_rating__icontains'
    )

    publisher: Optional[str] = Field(
        None, description='Filter books by publisher',
        q='publisher__name__icontains'
    )

    authors: Optional[str] = Field(
        None, description='Filter books by author',
        q='authors__name__icontains'
    )

    genres: Optional[str] = Field(
        None, description='Filter books by genre',
        q='genres__name__icontains'
    )

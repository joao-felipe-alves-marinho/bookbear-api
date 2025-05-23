from typing import Optional, List

from ninja import FilterSchema, ModelSchema
from pydantic import Field

from BookBearApi.models import Book
from BookBearApi.schemas.relationship_schema import AuthorRelationshipSchema, GenreRelationshipSchema, \
    PublisherRelationshipSchema
from BookBearApi.schemas.user_schema import ReviewBookSchema


class BookSchema(ModelSchema):
    authors: List[AuthorRelationshipSchema] = None
    genres: List[GenreRelationshipSchema] = None
    publisher: Optional[PublisherRelationshipSchema] = None
    reviews: List['ReviewBookSchema'] = None

    cover: Optional[str] = None

    class Meta:
        model = Book
        fields = ('id', 'title', 'publication_date', 'synopsis', 'score', 'age_rating', 'publisher', 'authors',
                  'genres')


class CreateBookSchema(ModelSchema):
    publisher: Optional[int] = None

    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'synopsis', 'age_rating', 'authors', 'genres')
        fields_optional = ('synopsis', 'authors', 'genres')


class UpdateBookSchema(ModelSchema):
    publisher: Optional[int] = None

    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'synopsis', 'age_rating', 'publisher', 'authors', 'genres')
        fields_optional = '__all__'


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

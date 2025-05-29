from typing import List, Optional

from ninja import ModelSchema

from BookBearApi.models import User, Author, Publisher, Book, Genre


class UserRelationshipSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class AuthorRelationshipSchema(ModelSchema):
    class Meta:
        model = Author
        fields = ('id', 'name', 'avatar')


class PublisherRelationshipSchema(ModelSchema):
    class Meta:
        model = Publisher
        fields = ('id', 'name', 'logo')


class GenreRelationshipSchema(ModelSchema):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class BookRelationshipSchema(ModelSchema):
    publisher: Optional[PublisherRelationshipSchema] = None
    authors: List[AuthorRelationshipSchema] = None

    class Meta:
        model = Book
        fields = ('id', 'title', 'score', 'age_rating', )

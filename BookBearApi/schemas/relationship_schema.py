from typing import List
from ninja_schema import ModelSchema

from BookBearApi.models import User, Author, Publisher, Book


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


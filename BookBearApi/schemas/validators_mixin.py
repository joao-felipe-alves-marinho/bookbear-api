from django.core.validators import validate_email
from ninja_schema import model_validator

from BookBearApi.models import User


class UniqueNameMixin:
    @classmethod
    @model_validator('name')
    def validate_unique_name(cls, value: str) -> str:
        model = cls.Config.model
        if model.objects.filter(name=value).exists():
            raise ValueError(f'{model.__name__} with name "{value}" already exists')
        return value


class UniqueEmailMixin:
    @classmethod
    @model_validator('email')
    def validate_email(cls, value):
        if User.objects.filter(email=value).exclude(id=cls.instance.id).exists():
            raise ValueError('Email already exists')
        validate_email(value)
        return value

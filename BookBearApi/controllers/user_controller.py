from typing import List

from django.shortcuts import aget_object_or_404
from ninja import Query
from ninja.pagination import paginate
from ninja_extra import (
    api_controller,
    ControllerBase,
    route, permissions
)
from ninja_extra.ordering import ordering, Ordering

from BookBearApi.models import User
from BookBearApi.schemas import UserSchema, FilterUserSchema, AsyncPageNumberPagination


@api_controller('/user', tags=['user'], permissions=[permissions.AllowAny], auth=None)
class UserController(ControllerBase):
    @route.get('/', response=List[UserSchema])
    @paginate(AsyncPageNumberPagination)
    @ordering(Ordering, ordering_fields=['username'])
    async def get_users(self, filters: FilterUserSchema = Query(...)):
        """
        Get a list of users.
        :return: List[UserSchema]
        """
        return [user async for user in filters.filter(User.objects.all())]

    @route.get('/{int:user_id}', response=UserSchema)
    async def get_user(self, user_id: int):
        """
        Get a user by id.
        :param user_id: int
        :return: UserSchema
        """
        return await aget_object_or_404(User, id=user_id)
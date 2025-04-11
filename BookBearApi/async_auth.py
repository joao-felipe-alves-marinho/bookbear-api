from typing import Any, Type

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.utils.module_loading import import_string
from ninja_extra.security import AsyncHttpBearer

from dj_ninja_auth.jwt import app_settings
from dj_ninja_auth.jwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from dj_ninja_auth.jwt.tokens import Token


class AsyncJWTBaseAuthentication:
    def __init__(self) -> None:
        super().__init__()
        self.user_model = get_user_model()

    @classmethod
    async def get_validated_token(cls, raw_token) -> Type[Token]:
        messages = []
        for AuthToken in app_settings.TOKEN_CLASSES:
            AuthToken = import_string(AuthToken)
            try:
                # Wrap the synchronous call with sync_to_async
                token = await sync_to_async(AuthToken)(raw_token)
                return token
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise InvalidToken(
            {
                "detail": "Given token not valid for any token type",
                "messages": messages,
            }
        )

    async def get_user(self, validated_token) -> AbstractBaseUser:
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[app_settings.USER_ID_CLAIM]
        except KeyError as e:
            raise InvalidToken(
                "Token contained no recognizable user identification"
            ) from e

        try:
            user = await self.user_model.objects.aget(**{app_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist as e:
            raise AuthenticationFailed("User not found") from e

        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        return user

    async def jwt_authenticate(self, request: HttpRequest, token: str) -> AbstractBaseUser:
        request.user = AnonymousUser()
        validated_token = await self.get_validated_token(token)
        user = await self.get_user(validated_token)
        request.user = user
        return user


class AsyncJWTAuth(AsyncJWTBaseAuthentication, AsyncHttpBearer):
    async def authenticate(self, request: HttpRequest, token: str) -> Any:
        return await self.jwt_authenticate(request, token)
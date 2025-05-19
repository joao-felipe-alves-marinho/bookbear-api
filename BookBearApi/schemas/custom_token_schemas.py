from typing import Optional, Type, cast, Dict

from dj_ninja_auth.jwt import app_settings
from dj_ninja_auth.jwt.tokens import RefreshToken
from dj_ninja_auth.jwt.schema import JWTTokenInputSchemaMixin
from dj_ninja_auth.schema import SuccessMessageMixin, LoginInputSchema
from django.contrib.auth.models import update_last_login, AbstractUser
from ninja import Schema

from BookBearApi.schemas.user_schema import UserSchema


class TokenRefreshOutputCookieSchema(Schema):
    access: str


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

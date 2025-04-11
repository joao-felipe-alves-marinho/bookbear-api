import os
from http import HTTPStatus

from dotenv import load_dotenv
from asgiref.sync import sync_to_async
from dj_ninja_auth import app_settings
from dj_ninja_auth.jwt.schema_control import JWTSchemaControl
from dj_ninja_auth.jwt.tokens import RefreshToken
from dj_ninja_auth.schema_control import SchemaControl
from django.conf import settings
from django.contrib.auth import alogin as django_alogin
from django.contrib.auth import alogout as django_alogout

from ninja import File
from ninja.files import UploadedFile
from ninja_extra import ControllerBase, api_controller, http_post, http_generic, route
from ninja_extra.exceptions import APIException
from ninja_extra.permissions import AllowAny, IsAuthenticated

from BookBearApi.models import User
from BookBearApi.schemas import TokenRefreshOutputCookieSchema, UserSchema, CreateUserSchema

load_dotenv()
schema = SchemaControl()
jwt_schema = JWTSchemaControl()


class AsyncJWTAuthenticationController(ControllerBase):
    auto_import = False

    @http_post(
        "/login",
        response={200: jwt_schema.pair_schema.get_response_schema()},
        auth=None,
        url_name="login",
    )
    async def login(self, credentials: jwt_schema.pair_schema):
        """Logs in a user

        Args:
            credentials (schema.login_schema): The login Credentials, typically username and/or email, and password

        Returns:
            JSON: A JSON object with the user's details
        """
        credentials.post_validate_schema()
        await django_alogin(self.context.request, credentials._user)
        kwargs = {
            "user": credentials._user,
            "access": credentials._access,
            "refresh": credentials._refresh if not settings.REFRESH_TOKEN_ON_COOKIE else "On Cookie",
        }
        self.context.response.set_cookie(
            "refresh",
            credentials._refresh,
            httponly=True,
            samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
            secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
            max_age=int(os.environ.get('AUTH_JWT_REFRESH_TOKEN_LIFETIME', 1)) * 86400
        )

        return await sync_to_async(credentials.to_response_schema)(**kwargs)

    @http_generic(
        "/logout",
        methods=["POST"],
        permissions=[IsAuthenticated],
        response={200: schema.success_schema},
        url_name="logout",
    )
    async def logout(self):
        """Logs out the user by flushing session data from the request

        Returns:
            JSON: A success message for a logged-out user
        """
        await django_alogout(self.context.request)
        self.context.response.set_cookie(
            "refresh",
            '',
            httponly=True,
            samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
            secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        )
        self.context.response.delete_cookie("refresh")
        return await sync_to_async(schema.success_schema)()

    # Get me
    @http_generic(
        "/me",
        methods=["GET"],
        permissions=[IsAuthenticated],
        response={200: UserSchema},
        url_name="me",
    )
    async def me(self):
        """Get the current user

        Returns:
            JSON: The current user's details
        """
        return self.context.request.user


class AsyncPasswordResetController(ControllerBase):
    auto_import = False

    @http_post(
        "/password/reset/request",
        response={200: schema.password_reset_request_schema.get_response_schema()},
        auth=None,
        url_name="password_reset_request",
    )
    async def password_reset_request(
            self, reset_request: schema.password_reset_request_schema
    ):
        """
        Requests a password reset on behalf of an unauthenticated user.

        Args:
            reset_request (schema.password_reset_request_schema): Contains the user's email.

        Returns:
            JSON: A success message confirming the request.
        """
        # Wrap the synchronous form.save() in sync_to_async so it doesn't block.
        await sync_to_async(reset_request._form.save)(
            request=self.context.request,
            email_template_name="password/reset_email.html",
            extra_email_context={"password_reset_url": app_settings.PASSWORD_RESET_URL},
        )
        return await sync_to_async(reset_request.to_response_schema)()

    @http_post(
        "/password/reset/confirm",
        response={200: schema.password_reset_confirm_schema.get_response_schema()},
        auth=None,
        url_name="password_reset_confirm",
    )
    async def password_reset_confirm(
            self, reset_confirm: schema.password_reset_confirm_schema
    ):
        """
        Resets the user's password using the new credentials and the reset token.

        Args:
            reset_confirm (schema.password_reset_confirm_schema): Contains token, uid, and new password data.

        Returns:
            JSON: A success message indicating the password was changed.
        """
        # If _form.save() is a synchronous operation, wrap it with sync_to_async.
        return await sync_to_async(reset_confirm.to_response_schema)()


class AsyncPasswordChangeController(ControllerBase):
    auto_import = False

    @http_post(
        "/password/change",
        response={200: schema.password_change_schema.get_response_schema()},
        permissions=[IsAuthenticated],
        url_name="password_change",
    )
    async def password_change(self, passwords: schema.password_change_schema):
        """A self-service for an authenticated user to change their own password

        Args:
            passwords (schema.password_change_schema): The user's credentials such as their `username`, `old_password` and 2 entries of their `new_password`.

        Returns:
            JSON: A success message to indicate the password has been changed successfully.
        """
        return await sync_to_async(passwords.to_response_schema)()


class AsyncJWTTokenRefreshController(ControllerBase):
    auto_import = False

    @http_post(
        "/cookie/refresh",
        url_name="token_refresh_cookie",
        response=TokenRefreshOutputCookieSchema,
        auth=None,
    )
    async def refresh_token_cookie(self):
        """Consumes a refresh token and returns a new `access`, `refresh` token pair.

        Returns:
            JSON: A JSON object with the new tokens
        """
        refresh_cookie = self.context.request.COOKIES.get('refresh')
        if not refresh_cookie:
            raise RefreshTokenNotOnCookieException()
        refresh = await sync_to_async(RefreshToken)(refresh_cookie)
        return {"access": str(refresh.access_token)}

    @http_post(
        "/refresh",
        response={200: jwt_schema.refresh_schema.get_response_schema()},
        auth=None,
        url_name="token_refresh",
    )
    async def refresh_token(self, token: jwt_schema.refresh_schema):
        """Consumes a refresh token and returns a new `access`, `refresh` token pair.

        Args:
            token (jwt_schema.refresh_schema): The `refresh` token.

        Returns:
            JSON: A JSON object with the new tokens
        """
        return await sync_to_async(token.to_response_schema)()


class AsyncJWTTokenVerificationController(ControllerBase):
    auto_import = False

    @http_post(
        "/verify",
        response={200: schema.success_schema},
        url_name="token_verify",
    )
    async def verify_token(self, token: jwt_schema.verify_schema):
        """Verifies that the provided token is valid.

        Args:
            token (jwt_schema.verify_schema): The `access` or `refresh` token.

        Returns:
            JSON: A success object if the token is valid.
        """
        return await sync_to_async(token.to_response_schema)()


@api_controller("/auth", permissions=[AllowAny], tags=["auth"])
class AsyncNinjaAuthJWTController(
    AsyncJWTAuthenticationController,
    AsyncPasswordResetController,
    AsyncPasswordChangeController,
    AsyncJWTTokenRefreshController,
    AsyncJWTTokenVerificationController
):
    auto_import = False

    @route.post('/register', response={201: UserSchema}, auth=None)
    async def register(self, payload: CreateUserSchema, avatar: File[UploadedFile] = None):
        user = await sync_to_async(User.objects.create_user)(
            avatar=avatar,
            **payload.dict(exclude_unset=True)
        )
        return HTTPStatus.CREATED, user


class RefreshTokenNotOnCookieException(APIException):
    status_code = HTTPStatus.BAD_REQUEST
    default_detail = "Refresh token is not on cookie."
    default_code = "refresh_token_not_on_cookie"

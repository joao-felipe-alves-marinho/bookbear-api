from ninja_extra import (
    NinjaExtraAPI
)

from .async_auth import AsyncJWTAuth
from .controllers import AsyncNinjaAuthJWTController, UserController, BookController, AdminController

api = NinjaExtraAPI(
    version='1.0.0',
    title='BookBear API',
    description='API para o projeto BookBear',
    auth=AsyncJWTAuth()
)

api.register_controllers(
    AsyncNinjaAuthJWTController,
    UserController,
    BookController,
    AdminController
)

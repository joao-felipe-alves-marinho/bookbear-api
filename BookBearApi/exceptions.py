from http import HTTPStatus

from ninja_extra.exceptions import APIException


class EmailAlreadyExistsException(APIException):
    status_code = HTTPStatus.CONFLICT
    default_detail = "Email already exists in the system."
    default_code = "email_already_exists"

class NameAlreadyExistsException(APIException):
    status_code = HTTPStatus.CONFLICT
    default_detail = "Name already exists in the system."
    default_code = "name_already_exists"
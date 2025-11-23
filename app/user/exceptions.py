from rest_framework import status

from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "not found"
    default_detail = "Not Found"


class UserIsNotActive(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "forbidden"
    default_detail = "Forbidden"


class WrongPassword(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "bad request"
    default_detail = "Bad Request"


class RefreshTokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "unauthorized"
    default_detail = "Unauthorized"


class RefreshTokenIsNotActive(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "unauthorized"
    default_detail = "Unauthorized"


class UserNotFound(NotFound):
    default_detail = "Пользователь не найден"


class RoleNotFound(NotFound):
    default_detail = "Роль не найдена"

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from jose import jwt

from user.models import User
from user.security import get_auth_data


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return None
        
        auth_data = get_auth_data()
        
        try:
            payload = jwt.decode(token, auth_data["secret_key"], auth_data["algorithm"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Время жизни токена истекло')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Некорректный токен')
        
        try:
            user = User.objects.get(id=payload["id"])
        except User.DoesNotExist:
            raise AuthenticationFailed('Пользователь не найден')

        return (user, token)
        

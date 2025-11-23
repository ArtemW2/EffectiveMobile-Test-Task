from datetime import datetime, timedelta

import bcrypt

from jose import jwt

from django.conf import settings

from user.models import UserRefreshToken, User


def get_auth_data() -> dict:
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


def get_hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed.encode("utf-8"),
    )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=7)
    to_encode.update({"exp": int(expire.timestamp())})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, key=auth_data["secret_key"], algorithm=auth_data["algorithm"])

    return encode_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=30)
    to_encode.update({"exp": int(expire.timestamp())})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, key=auth_data["secret_key"], algorithm=auth_data["algorithm"])

    return encoded_jwt


def generate_tokens(user: User) -> dict:
    access_token = create_access_token({"id": user.id})
    refresh_token = create_refresh_token({"id": user.id})

    refresh_token_record = UserRefreshToken.objects.create(refresh_token=refresh_token, user=user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

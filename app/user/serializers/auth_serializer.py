from rest_framework.serializers import ModelSerializer, Serializer, CharField, EmailField
from user.models import User

class RegisterSerializer(ModelSerializer):
    confirm_password = CharField(min_length=8, required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "surname", "email", "password", "confirm_password")
        read_only_fields = ("id",)


class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(min_length=8, required=True, write_only=True)


class RefreshTokenSerializer(Serializer):
    refresh_token = CharField()
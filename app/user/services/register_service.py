from user.models import User, Role

from user.serializers.user_serializer import UserSerializer

from user.security import get_hash_password

from rest_framework.exceptions import ValidationError


class RegisterService:
    @staticmethod
    def create_user_profile(data):
        try:
            password = data.pop("password")
            confirm_password = data.pop("confirm_password")

            if password != confirm_password:
                raise ValidationError("Пароли не совпадают")
            
            hash_password = get_hash_password(password)

            user = User.objects.create(**data)

            role = Role.objects.get(name="Гость")

            user.role = role
            user.password = hash_password
            user.save()

            return UserSerializer(user).data    
        
        except Exception:
            raise 
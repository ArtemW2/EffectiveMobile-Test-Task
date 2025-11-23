from rest_framework.serializers import ModelSerializer, CharField, BooleanField

from user.models import User

from user.services.role_service import RoleService

from user.serializers.role_serializer import RoleSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "surname", "email")

    
class UserSerializerForAdmin(UserSerializer):
    role = CharField()
    is_active = BooleanField()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "surname", "email", "role", "is_active")


class AdminUpdateUserSerializer(ModelSerializer):
    role = CharField(required=False)
    is_active = BooleanField(required=False)

    class Meta:
        model = User
        fields = ("role", "is_active")

    def validate_role(self, value):
        role = RoleService.get_role_by_name(value)
        return role


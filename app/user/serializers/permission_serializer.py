from rest_framework.serializers import ModelSerializer

from user.models import Permission

class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "name", "description")


class PermissionUpdateSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ("name", "description")
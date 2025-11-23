from rest_framework.serializers import ModelSerializer, ListField, CharField, StringRelatedField, IntegerField

from user.models import Role

from user.services.permission_service import PermissionService

class RoleSerializer(ModelSerializer):
    permissions = StringRelatedField(many=True)
    level = IntegerField(required=False)

    class Meta:
        model = Role
        fields = ("id", "name", "description", "level", "permissions")
            

class RoleUpdateSerializer(ModelSerializer):
    permissions = ListField(child=CharField(), required=False)

    class Meta:
        model = Role
        fields = ("name", "description", "level", "permissions")

    def validate_permissions(self, permissions):
        result_list = []
        for permission in permissions:
            permission_record = PermissionService.get_permission_by_name(permission)

            result_list.append(permission_record)

        return result_list

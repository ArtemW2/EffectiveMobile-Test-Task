from django.shortcuts import get_object_or_404

from user.models import Permission

from user.serializers.permission_serializer import PermissionSerializer


class PermissionService:
    @staticmethod
    def get_permissions():
        return Permission.objects.all()
    
    
    @staticmethod
    def get_permission_by_id(permission_id):
        return get_object_or_404(Permission, id=permission_id)


    @staticmethod
    def get_permission_by_name(permission_name):
        return get_object_or_404(Permission, name=permission_name)


    @staticmethod
    def create_permission(data):
        permission = Permission.objects.create(**data)

        return PermissionSerializer(permission).data
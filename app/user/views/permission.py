from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from user.services.permission_service import PermissionService

from user.serializers.permission_serializer import PermissionSerializer, PermissionUpdateSerializer

from user.permissions.permissions_permission import PermissionPermission
# from user.permissions.level_permission import MinimumLevelPermissionFactory

class PermissionView(APIView):
    """
    Создание новых прав доступа, в последствии применяемых к ролям пользователей.
    Уровень доступа: 
        - Спец.тех.поддержки (Просмотр списка существующих прав доступа)
        - Администратор (Просмотр всего списка, создание нового разрешения, удаление всего списка)
    """

    permission_classes = [IsAuthenticated, PermissionPermission]

    def get(self, request, *args, **kwargs):
        permissions = PermissionService.get_permissions() 

        response_data = PermissionSerializer(permissions, many=True).data

        return Response(response_data, status=status.HTTP_200_OK)
    
    
    def post(self, request, *args, **kwargs):
        serializer = PermissionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        permission = PermissionService.create_permission(serializer.validated_data)

        return Response(permission, status=status.HTTP_201_CREATED)
    


class PermissionDetail(APIView):
    """
    Работа с конкретным объектом права доступа.
    Уровень доступа: 
        - Спец.тех.поддержки (Просмотр информации о разрешении)
        - Администратор (Просмотр информации, корректировка описания, удаление права доступа)
    """

    permission_classes = [IsAuthenticated, PermissionPermission]

    def get(self, request, permission_id, *args, **kwargs):
        permission = PermissionService.get_permission_by_id(permission_id)
        
        response = PermissionSerializer(permission).data

        return Response(response, status=status.HTTP_200_OK)
    

    def patch(self, request, permission_id, *args, **kwargs):
        permission = PermissionService.get_permission_by_id(permission_id)

        serializer = PermissionUpdateSerializer(permission, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        response = PermissionSerializer(permission).data

        return Response(response, status=status.HTTP_200_OK)

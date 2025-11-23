from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from user.services.role_service import RoleService

from user.serializers.role_serializer import RoleSerializer, RoleUpdateSerializer

from user.permissions.permissions_permission import RolePermission
from user.permissions.level_permission import MinimumLevelPermissionFactory


class RoleView(APIView):
    """
    Создание новых ролей, в последствии назначемых пользователям.
    Уровень доступа: 
        - Спец.тех.поддержки (Просмотр списка ролей)
        - Администратор (Просмотр всего списка, создание новой роли)
    """

    permission_classes = [IsAuthenticated, MinimumLevelPermissionFactory(3), RolePermission]

    def get(self, request, *args, **kwargs):
        roles = RoleService.get_roles()

        response_data = RoleSerializer(roles, many=True).data

        return Response(response_data, status=status.HTTP_200_OK)
    
    
    def post(self, request, *args, **kwargs):
        serializer = RoleUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        role = RoleService.create_role(serializer.validated_data)

        response = RoleSerializer(role).data

        return Response(response, status=status.HTTP_201_CREATED)
    

class RoleDetail(APIView):
    """
    Работа с конкретной ролью.
    Уровень доступа: 
        - Спец.тех.поддержки (Просмотр информации о роли)
        - Администратор (Просмотр информации, корректировка описания, удаление роли)
    """

    permission_classes = [IsAuthenticated, RolePermission]

    def get(self, request, role_id, *args, **kwargs):
        role = RoleService.get_role_by_id(role_id)

        return Response(RoleSerializer(role).data, status=status.HTTP_200_OK)
    

    def patch(self, request, role_id, *args, **kwargs):
        role = RoleService.get_role_by_id(role_id)

        serializer = RoleUpdateSerializer(role, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        response = RoleSerializer(role).data

        return Response(response, status=status.HTTP_200_OK)

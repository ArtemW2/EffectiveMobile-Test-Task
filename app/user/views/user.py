from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from user.serializers.user_serializer import UserSerializer, UserSerializerForAdmin, AdminUpdateUserSerializer

from user.services.auth_service import AuthService

from user.permissions.permissions_permission import WorkOnUserPermission, WorkOnOwnAccountPermission

from rest_framework.permissions import IsAuthenticated


class AdminUserManagement(APIView):
    """ 
    Ручка для администраторов и технической поддержки
    Полный доступ ко всем данным пользователей
    """
    permission_classes = [IsAuthenticated, WorkOnUserPermission]

    def get(self, request, *args, **kwargs):
        guests, managers, programmers, supports, admins = AuthService.find_all()

        response_data = {
            "Администраторы": UserSerializerForAdmin(admins, many=True).data,
            "Техническая поддержка": UserSerializerForAdmin(supports, many=True).data,
            "Программисты": UserSerializerForAdmin(programmers, many=True).data,
            "Менеджеры": UserSerializerForAdmin(managers, many=True).data,
            "Гости": UserSerializerForAdmin(guests, many=True).data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AdminUserDetailManagement(APIView):
    """ 
    Ручка для администраторов и технической поддержки
    Полный доступ ко всем данным пользователей и возможность смены их ролей и деактивации аккаунтов
    """
    permission_classes = [IsAuthenticated, WorkOnUserPermission]

    def get(self, request, user_id, *args, **kwargs):
        user = AuthService.find_user_by_id(user_id)
        response_data = UserSerializerForAdmin(user).data
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    def patch(self, request, user_id, *args, **kwargs):
        user = AuthService.find_user_by_id(user_id)

        serializer = AdminUpdateUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        response = UserSerializerForAdmin(user).data

        return Response(response, status=status.HTTP_200_OK)


class UserOwnAccount(APIView):
    """
    Отдельная ручка для работы пользователя со своим аккаунтом. 
    В его возможности входит:
        1. Изменение ФИО или почтового адреса 
        (Можно добавить доп.проверку при помощи отправки кода подтверждения, в рамках данного тестового задания не стал это добавлять)
        2. Просмотр данных ФИО и почтового адреса
        3. Удаление своего аккаунта (Перевод его в статус "Не активен")
    """
    permission_classes = [IsAuthenticated, WorkOnOwnAccountPermission]
    
    def get(self, request, *args, **kwargs):
        response = UserSerializer(request.user).data
        return Response(response, status=status.HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
                
        response = { 
            "message": "Данные успешно изменены",
            "Измененные данные": UserSerializer(request.user).data
    
        }

        return Response(response, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        response = AuthService.logout_user(request)

        request.user.is_active = False
        request.user.save()

        return response
   
    
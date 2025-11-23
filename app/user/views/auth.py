from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from user.serializers.auth_serializer import RegisterSerializer, LoginSerializer, RefreshTokenSerializer

from user.services.register_service import RegisterService
from user.services.auth_service import AuthService

from rest_framework.permissions import IsAuthenticated

from user.permissions.auth_permission import IsAnonymous
from user.permissions.permissions_permission import RegisterPermission
from user.permissions.level_permission import MinimumLevelPermissionFactory


class UserRegister(APIView):
    permission_classes = [RegisterPermission | IsAnonymous]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = RegisterService.create_user_profile(serializer.validated_data)

        return Response(user, status=status.HTTP_201_CREATED)
    

class UserLogin(APIView):
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        response = AuthService.authenticate_user(serializer.validated_data["email"], serializer.validated_data["password"])

        return response
    

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = AuthService.logout_user(request)
        return response

    
class Refresh(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        response = AuthService.refresh_access_token(serializer.validated_data['refresh_token'])

        return response
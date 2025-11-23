from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta

from jose import jwt

from user.models import User

from user.security import verify_password, generate_tokens, get_auth_data

from user.models import UserRefreshToken

from user.exceptions import UserNotFound, UserIsNotActive, WrongPassword, RefreshTokenExpired, RefreshTokenIsNotActive

from rest_framework.response import Response

from rest_framework import status


class AuthService:
    @staticmethod
    def find_all():
        users = User.objects.select_related("role").prefetch_related("role__permissions").all()

        admins = users.filter(role__name="Администратор")
        supports = users.filter(role__name="Специалист технической поддержки")
        managers = users.filter(role__name="Менеджер")
        programmers = users.filter(role__name="Программист")
        guests = users.filter(role__name="Гость")

        return guests, managers, programmers, supports, admins


    @staticmethod
    def find_user_by_email(email):
        try:
            user = User.objects.select_related("role").prefetch_related("role__permissions").get(email=email)
        except User.DoesNotExist:
            raise UserNotFound("Не удалось идентифицировать пользователя")

        return user 
    

    @staticmethod
    def find_user_by_token(token):
        auth_data = get_auth_data()

        payload = jwt.decode(token, auth_data['secret_key'], auth_data['algorithm'])

        try:
            user = User.objects.select_related("role").prefetch_related("role__permissions").get(email=payload["email"])
        except User.DoesNotExist:
            raise UserNotFound("Не удалось идентифицировать пользователя")

        return user 


    @staticmethod
    def find_user_by_id(user_id):
        try:
            user = User.objects.select_related("role").prefetch_related("role__permissions").get(id=user_id)
        except User.DoesNotExist:
            raise UserNotFound("Не удалось идентифицировать пользователя")

        return user 


    @staticmethod
    def find_refresh_token(refresh_token):
        token = get_object_or_404(UserRefreshToken, refresh_token=refresh_token)

        return token


    @staticmethod
    def verify_user(user, password):
        if not verify_password(password, user.password):
            raise WrongPassword("Неверные входные данные")
        
        if user.is_active == False:
            raise UserIsNotActive("Вы не можете войти в аккаунт. Обратитесь к администратору")
        

    @staticmethod
    def authenticate_user(email, password):
        try:
            user = AuthService.find_user_by_email(email)
            
            AuthService.verify_user(user, password)

            tokens = generate_tokens(user)

            response = Response({"message": "Вы успешно вошли в систему"}, status=status.HTTP_200_OK)

            response.set_cookie(
                key = "access_token",
                value = tokens["access_token"],
                httponly = True,
                max_age = 7*24*60*60,
                samesite = 'Lax'
            )
            response.set_cookie(
                key = "refresh_token",
                value = tokens["refresh_token"],
                httponly = True,
                max_age = 30*24*60*60,
                samesite = 'Lax'
            )
            
            return response

        except User.DoesNotExist:
            raise ValueError("Пользователь не найден")
        

    @staticmethod
    def logout_user(request):
        response = Response({"message": "Вы успешно вышли из системы"}, status=status.HTTP_200_OK)

        refresh_token = request.COOKIES.get("refresh_token")

        refresh_token_record = get_object_or_404(UserRefreshToken, refresh_token=refresh_token)

        refresh_token_record.is_active = False
        refresh_token_record.save()

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
    

    @staticmethod
    def refresh_access_token(refresh_token):
        token = AuthService.find_refresh_token(refresh_token)

        if refresh_token.created_at + timedelta(days=30) < datetime.now():
            refresh_token.is_active = False
            refresh_token.save()
            raise RefreshTokenExpired("Время жизни токена истекло")
        
        if refresh_token.is_active == False:
            raise RefreshTokenIsNotActive("Токен не активен")
        
        user = AuthService.find_user_by_token(refresh_token.refresh_token)

        access_token = access_token({"id": user.id, "email": user.email})

        response = Response({"message": "Токен доступа успешно обновлён"}, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key = "access_token",
            value = access_token,
            httponly = True,
            max_age = 7*24*60*60,
            samesite = 'Lax'
        )

        return response
        
        
from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == "Менеджер"
    

class IsProgrammer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == "Программист"
    

class IsSupport(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == "Специалист технической поддержки"
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == "Администратор"
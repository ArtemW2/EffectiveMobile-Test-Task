from rest_framework.permissions import BasePermission

class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
    

class IsAccountOwner(BasePermission):
    def has_permission(self, request, view):
        return view.request.user == request.user
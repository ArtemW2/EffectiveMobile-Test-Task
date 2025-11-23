from rest_framework.permissions import BasePermission


class MinimumLevelPermission(BasePermission):
    def __init__(self, min_level):
        self.min_level = min_level

    def has_permission(self, request, view):
        user_level = request.user.role.level if request.user.role.level is not None else 0
        return user_level >= self.min_level
    

def MinimumLevelPermissionFactory(min_level):
    class _MinimumLevelPermission(MinimumLevelPermission):
        def __init__(self):
            super().__init__(min_level)
    return _MinimumLevelPermission



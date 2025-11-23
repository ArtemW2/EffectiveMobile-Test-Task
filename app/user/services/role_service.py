from user.models import Role

from user.exceptions import RoleNotFound


class RoleService:
    @staticmethod
    def get_roles():
        return Role.objects.all().prefetch_related("permissions")
    

    @staticmethod
    def get_role_by_id(role_id):
        try:
            role = Role.objects.prefetch_related("permissions").get(id=role_id)
        except Role.DoesNotExist:
            raise RoleNotFound("Роль не найдена")
        
        return role


    @staticmethod
    def get_role_by_name(role_name):
        try:
            role = Role.objects.prefetch_related("permissions").get(name=role_name)
        except Role.DoesNotExist:
            raise RoleNotFound("Роль не найдена")
        
        return role


    @staticmethod
    def create_role(data):
        role = Role.objects.create(**data)

        return role
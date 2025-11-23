from user.permissions.generic_permission import GenericPermission


class RolePermission(GenericPermission):
    def __init__(self):
        super().__init__(
            read_perm="CAN_READ_ROLES",
            create_perm="CAN_CREATE_ROLES",
            modify_perm="CAN_MODIFY_ROLE",
            delete_all_perm="CAN_DELETE_ALL_ROLES",
            delete_perm="CAN_DELETE_ROLE"
        )


class PermissionPermission(GenericPermission):
    def __init__(self):
        super().__init__(
            read_perm="CAN_READ_PERMISSIONS",
            create_perm="CAN_CREATE_PERMISSIONS",
            modify_perm="CAN_MODIFY_PERMISSION",
            delete_all_perm="CAN_DELETE_ALL_PERMISSIONS",
            delete_perm="CAN_DELETE_PERMISSION"
        )


class RegisterPermission(GenericPermission):
    def __init__(self):
        super().__init__(read_perm="CAN_CREATE_NEW_USER", create_perm="CAN_CREATE_NEW_USER")


class WorkOnUserPermission(GenericPermission):
    def __init__(self):
        super().__init__(
            read_perm="CAN_READ_WHOLE_USER_INFO", 
            modify_perm="CAN_CHANGE_ROLE_AND_DEACTIVATE_ACCOUNT"
        )

    def has_object_permission(self, request, view, obj):
        is_updated_user_level = obj.role.level 

        # Нельзя работать с собственным аккаунтом и с аккаунтами пользователей, чьи роли выше по уровню, чем у пользователя
        if request.user.role.level < is_updated_user_level or request.user == obj:
            return False 

        return super().has_permission(request, view)


class WorkOnOwnAccountPermission(GenericPermission):
    def __init__(self):
        super().__init__(
            read_perm="CAN_READ_OWN_USER_INFO",
            modify_perm="CAN_MODIFY_PERSONAL_DATA",
            delete_perm="CAN_DEACTIVATE_OWN_ACCOUNT"
        )

    # def has_permission(self, request, view):
    #     if request.method in ['POST']:
    #         return False
    #     return super().has_permission(request, view)
    
    # def has_object_permission(self, request, view, obj):
    #     if request.method in ['POST']:
    #         return False
    #     return super().has_object_permission(request, view, obj)
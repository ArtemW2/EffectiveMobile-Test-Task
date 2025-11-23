from rest_framework.permissions import BasePermission


class GenericPermission(BasePermission):
    def __init__(
        self, 
        read_perm = None, 
        create_perm = None, 
        modify_perm = None, 
        delete_perm = None
    ):
        self.read_perm = read_perm
        self.create_perm = create_perm
        self.modify_perm = modify_perm
        self.delete_perm = delete_perm


    def has_permission(self, request, view):
        if request.method == "GET":
            return self.read_perm is not None and request.user.has_permission(self.read_perm)

        if request.method == "POST":
            return self.create_perm is not None and request.user.has_permission(self.create_perm)

        if request.method == "PATCH":
            return self.modify_perm is not None and request.user.has_permission(self.modify_perm)

        if request.method == "DELETE":
            return self.delete_perm is not None and request.user.has_permission(self.delete_perm)

        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return self.read_perm is not None and request.user.has_permission(self.read_perm)

        if request.method == "PATCH":
            return self.modify_perm is not None and request.user.has_permission(self.modify_perm)

        if request.method == "DELETE":
            return self.delete_perm is not None and request.user.has_permission(self.delete_perm)

        return False
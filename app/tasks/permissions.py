from user.permissions.generic_permission import GenericPermission

from tasks.service import TaskService

class TaskPermission(GenericPermission):
    def __init__(self):
        super().__init__(
            read_perm="CAN_READ_TASK",
            create_perm="CAN_CREATE_TASKS",
            modify_perm="CAN_MODIFY_TASK",

        )

    
class IsMemberTask(GenericPermission):
    def has_permission(self, request, view):
        task = TaskService.find_by_id(view.kwargs["task_id"])

        if request.user == task.author or request.user == task.executor and request.method in ["GET", "PATCH"]:
            return True

        elif request.user == task.author and request.method == "DELETE":
            return True
        
        return super().has_permission(request, view)
    

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user == obj.executor and request.method in ["GET", "PATCH"]:
            return True

        if request.user == obj.author and request.method == "DELETE":
            return True
        
        return super().has_object_permission(request, view, obj)
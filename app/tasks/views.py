from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from tasks.serializers import (TasKSerializer, TaskCreateSerializerForAuthor,
    TaskUpdateSerializerForAuthor,  TaskUpdateSerializerForExecutor, TaskUpdateAdminSerializer)

from tasks.service import TaskService

from tasks.permissions import TaskPermission, IsMemberTask

from user.permissions.level_permission import MinimumLevelPermissionFactory


class TaskView(APIView):
    permission_classes = [IsAuthenticated, MinimumLevelPermissionFactory(1)]

    def get(self, request, *args, **kwargs):
        role_name = request.user.role.name 

        if role_name in ["Администратор", "Специалист технической поддержки"]:
            tasks = TaskService.find_all()
            response = TasKSerializer(tasks, many=True).data

        elif role_name == "Программист":
            own_tasks, executive_tasks = TaskService.find_programmer_tasks(request.user)
            response = {
                "Мои задачи(Автор)": TasKSerializer(own_tasks, many=True).data,
                "Исполняемые мной задачи": TasKSerializer(executive_tasks, many=True).data,
            }

        else:
            tasks = TaskService.find_manager_tasks(request.user)
            response = TasKSerializer(tasks, many=True).data

        return Response(response, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        serializer = TaskCreateSerializerForAuthor(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.validated_data["author"] = request.user
            task = TaskService.create_task(serializer.validated_data)

            response = TasKSerializer(task).data
            return Response(response, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetail(APIView):
    permission_classes = [IsAuthenticated, TaskPermission | IsMemberTask]

    def get(self, request, task_id, *args, **kwargs):
        task = TaskService.find_by_id(task_id)

        return Response(TasKSerializer(task).data, status=status.HTTP_200_OK)
    
    def patch(self, request, task_id, *args, **kwargs):
        task = TaskService.find_by_id(task_id)

        if request.user == task.author and request.user.role.level < 3:
            serializer = TaskUpdateSerializerForAuthor(task, data=request.data)

        elif request.user == task.executor:
            serializer = TaskUpdateSerializerForExecutor(task, data=request.data)

        else:
            serializer = TaskUpdateAdminSerializer(task, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(TasKSerializer(task).data, status=status.HTTP_200_OK)


    def delete(self, request, task_id, *args, **kwargs):
        task = TaskService.find_by_id(task_id)

        task.delete()
        return Response({"message": "Задача удалена"}, status=status.HTTP_204_NO_CONTENT)


from tasks.models import Task

from django.db.models import Q

class TaskService:
    @staticmethod
    def find_all():
        return Task.objects.all().select_related("author", "executor")
    

    @staticmethod
    def find_programmer_tasks(user):
        tasks = Task.objects.filter(Q(author=user) | Q(executor=user) ).select_related("author", "executor")

        own_tasks = tasks.filter(author=user)
        executive_tasks = tasks.filter(executor=user)

        return own_tasks, executive_tasks
    
    
    @staticmethod
    def find_manager_tasks(user):
        tasks = Task.objects.filter(author=user).select_related("author", "executor")

        return tasks


    # @staticmethod
    # def find_participate_tasks(user):
    #    tasks = Task.objects.filter(Q(author=user) | Q(executor=user)).select_related("author", "executor")

    #    my_tasks = tasks.filter(author=user)
    #    executive_tasks = tasks.filter(executor=user)

    #    return my_tasks, executive_tasks


    @staticmethod
    def find_tasks_without_executor():
        return Task.objects.filter(executor=None).select_related("author")


    @staticmethod
    def find_by_id(task_id):
        try:
            task = Task.objects.select_related("author", "executor").get(id=task_id)

        except Task.DoesNotExist:
            raise ValueError("Задачи не найдена")
        
        return task


    @staticmethod
    def create_task(data):
        task = Task.objects.create(**data)

        return task
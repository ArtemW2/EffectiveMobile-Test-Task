from rest_framework.serializers import ModelSerializer, CharField, DateField, ValidationError, IntegerField
from user.models import User
from tasks.models import Task

from user.serializers.user_serializer import UserSerializer

class TasKSerializer(ModelSerializer):
    author = UserSerializer()
    executor = UserSerializer()

    class Meta:
        model = Task
        fields = ("id", "title", "content", "author", "executor", "status", "priority", "created_at", "expired_at")


class TaskCreateSerializerForAuthor(ModelSerializer):
    title = CharField()
    content = CharField(required=False)

    class Meta:
        model = Task
        fields = ("title", "content")


class TaskUpdateSerializerForAuthor(ModelSerializer):
    title = CharField(required=False)
    content = CharField(required=False)

    class Meta:
        model = Task
        fields = ("title", "content")


class TaskUpdateSerializerForExecutor(ModelSerializer):
    class Meta:
        model = Task
        fields = ("status",)


class TaskUpdateAdminSerializer(TaskUpdateSerializerForAuthor):
    priority = CharField(required=False)
    expired_at = DateField(required=False)
    executor = IntegerField(required=False)

    class Meta:
        model = Task
        fields = ("title", "content", "executor", "priority", "expired_at")

    def validate_executor(self, value):
        try:
            executor_id = value
            executor = User.objects.get(id=executor_id)

            if executor.role.name != "Программист":
                raise ValidationError("Исполнителем задачи может быть только программист")

        except (ValueError, User.DoesNotExist) as e:
            raise ValidationError(f"Invalid executor: {str(e)}")
        
        return executor

    def save(self, *args, **kwargs):
        executor = self.validated_data.get("executor")
        if executor:
            self.instance.executor = executor
        else:
            self.instance.executor = None
        super().save(*args, **kwargs)

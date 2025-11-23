from datetime import timedelta, date

from django.utils import timezone
from django.db import models

from user.models import User


class StatusChoices(models.TextChoices):
    CANCELED = "canceled", "Canceled"
    DEFAULT = "default", "Default"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"


class PriorityChoices(models.TextChoices):
    LOW = "low", "LOW"
    DEFAULT = "default", "DEFAULT"
    HIGH = "high", "HIGH"
    HIGHEST = "highest", "HIGHEST"


class Task(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_tasks")
    executor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="executive_tasks")

    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.DEFAULT.value)
    priority = models.CharField(choices=PriorityChoices.choices, default=PriorityChoices.DEFAULT.value)

    created_at = models.DateField(auto_now_add=True)
    expired_at = models.DateField(blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.created_at = date.today()
            self.expired_at = self.created_at + timedelta(days=7)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title}. Автор - {self.author}"
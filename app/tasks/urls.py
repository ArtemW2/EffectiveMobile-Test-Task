from django.urls import path

from tasks.views import TaskView, TaskDetail

urlpatterns = [
    path("api/tasks/", TaskView.as_view(), name="tasks"),
    
    path("api/tasks/<int:task_id>/", TaskDetail.as_view(), name='task-detail')
]
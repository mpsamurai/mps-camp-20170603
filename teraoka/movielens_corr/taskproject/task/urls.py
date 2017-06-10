from django.conf.urls import url
from task.views import TaskStart, TaskList

urlpatterns = [
    url(r'^$', TaskStart.as_view()),
    url(r'^enddisplay/', TaskList.as_view())
]
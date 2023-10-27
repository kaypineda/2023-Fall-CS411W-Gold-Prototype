from django.urls import path
from . import views

app_name = 'AppCalendar'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('task/new/', views.task, name='task_new'),
	path('task/edit/(?P<task_id>\d+)/', views.task, name='task_edit'),
]
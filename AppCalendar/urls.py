from django.urls import path
from . import views
from . import export_task

app_name = 'AppCalendar'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('task/new/', views.task, name='task_new'),
	path('task/edit/<int:task_id>/', views.task, name='task_edit'),
    # path('export/<str:format>/', views.export, name='export'),
    path('export/', export_task.export, name='export'),
]
from django.urls import path
from . import views
from . import export_task, import_task

app_name = 'AppCalendar'
urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('task/new/', views.task, name='task_new'),
	path('task/edit/<int:task_id>/', views.task, name='task_edit'),
    path('task/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('export/', export_task.export, name='export'),
    path('import/', import_task.import_file, name='import_file'),
]
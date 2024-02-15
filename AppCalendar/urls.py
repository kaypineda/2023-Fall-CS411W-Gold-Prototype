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
    #path('import/', import_task.import_csv, name='import_csv'),
    #path('calendar/list/', views.sidebar, name='sidebar'),
    path('import/', import_task.import_file, name='import_file'),
    path('convert_address_to_lat_lon/', convert_address_to_lat_lon, name='convert_address_to_lat_lon'),
    path('convert_lat_lon_to_address/', convert_lat_lon_to_address, name='convert_lat_lon_to_address'),
]

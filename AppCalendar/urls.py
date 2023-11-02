from django.urls import path
from . import views

app_name = 'AppCalendar'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.Event, name='event_new'),
	path('event/edit/(?P<event_id>\d+)/', views.Event, name='event_edit'),
]
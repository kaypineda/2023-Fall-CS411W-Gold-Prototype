from django.urls import path
from . import views

app_name = 'AppUser'
urlpatterns = [
    path('login/', views.login, name='login'),
]
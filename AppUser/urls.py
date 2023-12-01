from django.urls import path
from . import views

app_name = 'AppUser'
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.user_register, name='user_register'),
]
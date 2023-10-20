from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.aboutUs, name='about-us'),
    path('problem/', views.problem, name='problem'),
    path('deliverables/', views.deliverables, name='deliverables'),
    path('presentations/', views.presentations, name='presentations'),
    path('labs/', views.labs, name='labs'),
    path('references/', views.references, name='references'),
    path('registration/login/', views.login, name='login'),
]

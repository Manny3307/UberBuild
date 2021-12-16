from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page),
    path('login/', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('404/', views.Error404, name='404'),
]
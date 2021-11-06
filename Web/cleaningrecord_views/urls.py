from django.urls import path
from .views import HomePageView, AboutPageView, LoginPageView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('', LoginPageView.as_view(), name='login'),
]
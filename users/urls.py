from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import HomePageView

app_name = UsersConfig.name
urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('logout/',LogoutView.as_view(),name='logout'),



]
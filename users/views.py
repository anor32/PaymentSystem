from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import TemplateView

from users.models import User


# Create your views here.


class HomePageView(TemplateView):
    model = User
    template_name = 'home.html'





class UserLogoutView(TemplateView):
    model = User
    success_url = '/'

class UserRegisterView(TemplateView):
    template_name = 'users/register.html'
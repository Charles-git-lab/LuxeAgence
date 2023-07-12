
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home, name="home"),
    path('login',log_in, name="login"),
    path('register',register, name="register"),
    path('logout',log_out, name="log_out"),
    path('contest',contest, name="contest"),
]

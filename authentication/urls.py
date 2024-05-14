
from django.urls import path
from .views import login
from django.contrib.auth.views import auth_logout

urlpatterns = [
    path('login', login, name="login"),
    path('logout/', auth_logout, name='logout'),

]

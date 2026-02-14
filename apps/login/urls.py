from django.urls import path
from .views import cadastro, home, login

urlpatterns = [
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login, name="login"),
    path("", home, name="home"),    
    
]

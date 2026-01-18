from django.urls import include, path
from login.views import cadastro, login

urlpatterns = [
    path("cadastro", cadastro, name="cadastro"),
    path("", login, name="login"),
    
]

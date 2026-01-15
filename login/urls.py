from django.urls import include, path
from login.views import Login

urlpatterns = [
    path("", Login.as_view(), name="login")
]

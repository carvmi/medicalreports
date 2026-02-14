from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def cadastro(request):
 if request.method == 'GET':
     return render(request, 'register.html') 
 else:
   username = request.POST.get('username')
   email = request.POST.get('email')
   password = request.POST.get('password')

   user = User.objects.filter(username=username).first()

   if User.objects.filter(username=username).exists():
     messages.error(request, "Usuário já existe.")
     return render(request, "login.html")

   user = User.objects.create_user(username=username, email=email, password=password)
   user.save()
   messages.error(request, "Usuário cadastrado com sucesso.")
   return render(request, "register.html")


def login(request):
 if request.method == 'GET':
     return render(request, 'login.html')
 else:
    username = request.POST.get('username')
    password = request.POST.get('password')
  
    user = authenticate(request, username=username, password=password)
  
    if user is not None:
        auth_login(request, user)
        return redirect('exams.eview')
    else:
        messages.error(request, "Usuário ou senha inválidos.")
        return render(request, "login.html")

def home(request):
  return render(request, 'home.html')  
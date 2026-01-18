from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


def cadastro(request):
 if request.method == 'GET':
     return render(request, 'register.html') 
 else:
   username = request.POST.get('username')
   email = request.POST.get('email')
   password = request.POST.get('password')

   user = User.objects.filter(username=username).first()

   if user:
     return HttpResponse('Usuário já existe')
   
   user = User.objects.create_user(username=username, email=email, password=password)
   user.save()
   return HttpResponse('Usuário cadastrado com sucesso!')


def login(request):
 return render(request, 'login.html')

def home(request):
 return render(request, 'home.html')
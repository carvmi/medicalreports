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

   user = User.objects.get(username=username)

   if user:
     return HttpResponse("Usuário já existe")
   else:
   return HttpResponse(username)

def login(request):
 return render(request, 'login.html')
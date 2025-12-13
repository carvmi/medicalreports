from django.shortcuts import render
from medprofiles.models import HealthProfessional
from django.http import HttpResponse

# Create your views here.
def medprofiles(request):
 medprofiles = HealthProfessional.objects.all()
 contexto = {
   'med_list': medprofiles
 }

 return render(
  request,
    'medprofiles.html',
    contexto
  )

def add(request):
 return render(
  request, 
  'medprofiles.html'
 )
def store(request):
 data = request.GET.dict()
 medpro = medprofiles.objects.create(**data)
 return HttpResponse ('Log no terminal')
from django.shortcuts import render
from medprofiles.models import Medprofiles

# Create your views here.
def medprofiles(request):
 medprofiles = Medprofiles.objects.all()
 contexto = {
   'med_list': medprofiles
 }

 return render(
  request,
    'medprofiles.html',
    contexto
  )
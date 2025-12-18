from django.shortcuts import render, redirect
from medprofiles.models import HealthProfessional

def index(request):
 return render (
    request, 'index.html'
 )

def add(request):
 if request.method == "POST":
        n = request.POST['full_name']
        p = request.POST['position']
        i = request.POST['institution']
        s = request.POST['specialization']
        r = request.POST['professional_registration']
        medpro = HealthProfessional(full_name=n, position=p, institution=i, specialization = s, professional_registration = r)
        medpro.save()
        #return redirect('medlist')
 return render(
  request, 
  'medform.html'
 )
def store(request):
 ...
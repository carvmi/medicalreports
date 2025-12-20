from django.shortcuts import render
from patients.models import Patient
from django.http import HttpResponse
from .forms import PatientForm

# Create your views here.

def pform(request):
 form = PatientForm()
 if request.method == 'POST':
  form = PatientForm(request.POST)
  if form.is_valid():
   form.save()
   return HttpResponse ("Sucess")
 return render(request, 'patients.html', {'form': form})
 
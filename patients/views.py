from django.shortcuts import render, redirect
from patients.models import Patient
from django.http import HttpResponse
from .forms import PatientForm

# Create your views here.

def plist(request):
    dados = Patient.objects.all()
    return render(
        request,
        'plist.html',
        {
            'dados':dados
        }
    ) 

def pform(request):
 form = PatientForm()
 if request.method == 'POST':
  form = PatientForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('plist')
 return render(request, 'pform.html', {'form': form})
 
from django.shortcuts import render
from patients.models import Patient
from patients.models import Mammogram
from django.http import HttpResponse
from .forms import PatientForm

# Create your views here.

def pform(request):
 form = PatientForm()
 if request.method == 'POST':
  form = PatientForm(request.POST)
  mammograms = request.FILES.getlist('mammograms')
  for mammogram in mammograms:
    Mammogram.objects.create(
      patient=Patient,
      image=mammogram
    )
  if form.is_valid():
   form.save()
   return HttpResponse ("Sucess")
 return render(request, 'pform.html', {'form': form})
 
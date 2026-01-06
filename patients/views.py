from django.shortcuts import render, redirect, get_object_or_404
from patients.models import Patient
from .forms import PatientForm

def view(request):
    dados = Patient.objects.all()
    return render(
        request,
        'plist.html',
        {
            'dados':dados
        }
    ) 

def create(request):
 form = PatientForm()
 if request.method == 'POST':
  form = PatientForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('view') 
 return render(request, 'pform.html', {'form': form})
 
def edit(request, id):
   patient = get_object_or_404(Patient, pk=id)
   form = PatientForm(instance=patient)
   if request.method == "POST":
    form = PatientForm(request.POST, instance=patient)
    if form.is_valid():
     form.save()
     return redirect('view')
   return render(request, 'pedit.html', {'form': form, 'patient': patient})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from .forms import PatientForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url='/login/')
def pview(request):
    dados = Patient.objects.filter(is_active=True)
    return render(
        request,
        'plist.html',
        {
            'dados':dados
        }
    ) 

def pcreate(request):
 form = PatientForm()
 if request.method == 'POST':
  form = PatientForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('p.view') 
 return render(request, 'pform.html', {'form': form})
 
def pedit(request, id):
   patient = get_object_or_404(Patient, pk=id, is_active=True)
   form = PatientForm(instance=patient)
   if request.method == "POST":
    form = PatientForm(request.POST, instance=patient)
    if form.is_valid():
     form.save()
     return redirect('p.view')
   return render(request, 'pedit.html', {'form': form, 'patient': patient})

def pdelete(request, id):
    patient = get_object_or_404(Patient, pk=id, is_active=True)
    patient.is_active = False
    patient.deleted_at = timezone.now()
    patient.save(update_fields=["is_active", "deleted_at"])
    return redirect('p.view')

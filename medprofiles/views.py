from django.shortcuts import render, redirect, get_object_or_404
from medprofiles.models import HealthProfessional
from .forms import MedForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url='/login/')
def view(request):
    med = HealthProfessional.objects.filter(is_active=True)
    return render(
        request,
        'medlist.html',
        {
            'med': med, 
        }
    ) 

def create(request):
 form = MedForm()
 if request.method == 'POST':
  form = MedForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('med.view') 
 return render(request, 'medform.html', {'form': form})
 
def edit(request, id):
   healthprofessional = get_object_or_404(HealthProfessional, pk=id, is_active=True)
   form = MedForm(instance=healthprofessional)
   if request.method == "POST":
    form = MedForm(request.POST, instance=healthprofessional)
    if form.is_valid():
     form.save()
     return redirect('med.view')
   return render(request, 'mededit.html', {'form': form, 'healthprofessional': healthprofessional})

def delete(request, id):
    med = get_object_or_404(HealthProfessional, pk=id, is_active=True)
    med.is_active = False
    med.deleted_at = timezone.now()
    med.save(update_fields=["is_active", "deleted_at"])
    return redirect('med.view')

from django.shortcuts import render, redirect, get_object_or_404
from institution.models import Institution
from medprofiles.models import HealthProfessional

def view(request):
    med = HealthProfessional.objects.all()
    inst = Institution.objects.all()
    return render(
        request,
        'plist.html',
        {
            'med': med, 
            'inst': inst
        }
    ) 

def create(request):
 form = MedForm()
 if request.method == 'POST':
  form = MedForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('view') 
 return render(request, 'pform.html', {'form': form})
 
def edit(request, id):
   medprofiles = get_object_or_404(HealthProfessional, pk=id)
   form = MedForm(instance=medprofiles)
   if request.method == "POST":
    form = MedForm(request.POST, instance=medprofiles)
    if form.is_valid():
     form.save()
     return redirect('view')
   return render(request, 'mededit.html', {'form': form, 'medprofiles': medprofiles})

def delete(request, id):
    med = get_object_or_404(HealthProfessional, pk=id)
    med.delete()
    return redirect('view')
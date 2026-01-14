from django.shortcuts import render, redirect, get_object_or_404
from institution.models import Institution, Address
from .forms import InstForm, AddressForm

def view(request):
    dados = Institution.objects.all()
    return render(
        request,
        'instlist.html',
        {
            'dados':dados,
        }
    ) 

def create(request):
 form = InstForm()
 if request.method == 'POST':
  form = InstForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('inst.view') 
 return render(request, 'instform.html', {'form': form})

def adcreate(request):
 address = Address.objects.all()
 form = AddressForm()
 if request.method == 'POST':
  form = AddressForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('inst.view') 
 return render(request, 'adform.html', {'form': form, 'address': address})
 
def edit(request, id):
   inst = get_object_or_404(Institution, pk=id)
   form = InstForm(instance=inst)
   if request.method == "POST":
    form = InstForm(request.POST, instance=inst)
    if form.is_valid():
     form.save()
     return redirect('inst.view')
   return render(request, 'instedit.html', {'form': form, 'inst': inst})

def delete(request, id):
    inst = get_object_or_404(Institution, pk=id)
    inst.delete()
    return redirect('inst.view')
 
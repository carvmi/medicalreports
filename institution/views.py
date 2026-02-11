from django.shortcuts import render, redirect, get_object_or_404
from institution.models import Institution, Address
from .forms import InstForm, AddressForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url='/login/')
def iview(request):
    dados = Institution.objects.filter(is_active=True)
    return render(
        request,
        'instlist.html',
        {
            'dados':dados,
        }
    ) 

def icreate(request):
 form = InstForm()
 if request.method == 'POST':
  form = InstForm(request.POST, request.FILES)
  if form.is_valid():
   form.save()
   return redirect('inst.iview') 
 return render(request, 'instform.html', {'form': form})

def adcreate(request):
 address = Address.objects.filter(is_active=True)
 form = AddressForm()
 if request.method == 'POST':
  form = AddressForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('inst.iview') 
 return render(request, 'adform.html', {'form': form, 'address': address})
 
def iedit(request, id):
   inst = get_object_or_404(Institution, pk=id, is_active=True)
   form = InstForm(instance=inst)
   if request.method == "POST":
    form = InstForm(request.POST, request.FILES, instance=inst)
    if form.is_valid():
     form.save()
     return redirect('inst.iview')
   return render(request, 'instedit.html', {'form': form, 'inst': inst})

def idelete(request, id):
    inst = get_object_or_404(Institution, pk=id, is_active=True)
    inst.is_active = False
    inst.deleted_at = timezone.now()
    inst.save(update_fields=["is_active", "deleted_at"])
    return redirect('inst.iview')
 

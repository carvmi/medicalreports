from django.shortcuts import render
from patients.models import Patient

# Create your views here.
def patients(request):
 return render(
  request,
    'patients.html'
  )
 
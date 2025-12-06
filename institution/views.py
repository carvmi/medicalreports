from django.shortcuts import render
from institution.models import Institution

# Create your views here.
def institution(request):
 institutions = Institution.objects.all()
 contexto = {
   'inst_list': institutions
 }

 return render(
  request,
    'institution.html',
    contexto
  )
 
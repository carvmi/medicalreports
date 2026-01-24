from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MammogramExamForm
from exams.models import MammogramExam
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def eview(request):
    if request.user.is_authenticated:
     dados = MammogramExam.objects.all()
     return render(
        request,
        'list.html',
        {
            'dados':dados,
        }
     ) 
    return HttpResponse('Você precisa estar logado para acessar esta página.')
    

def ecreate(request):
 form = MammogramExamForm()
 if request.method == 'POST':
  form = MammogramExamForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('exams.eview') 
 return render(request, 'form.html', {'form': form})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def estore(request):
    if request.method == 'POST':
        form = MammogramExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user_ip = get_client_ip(request)
            exam.save()
            return redirect('exams.view')

    return redirect('exams.ecreate')

def eedit(request, id):
   exams = get_object_or_404(MammogramExam, pk=id)
   form = MammogramExamForm(instance=exams)
   if request.method == "POST":
    form = MammogramExamForm(request.POST, instance=exams)
    if form.is_valid():
     form.save()
     return redirect('exams.eview')
   return render(request, 'edit.html', {'form': form, 'exams': exams})

def edelete(request, id):
    exams = get_object_or_404(MammogramExam, pk=id)
    exams.delete()
    return redirect('exams.eview')
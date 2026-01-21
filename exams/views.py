from django.shortcuts import render, redirect, get_object_or_404
from .forms import MammogramExamForm
from exams.models import MammogramExam

def view(request):
    dados = MammogramExam.objects.all()
    return render(
        request,
        'list.html',
        {
            'dados':dados,
        }
    ) 

def create(request):
 form = MammogramExamForm()
 if request.method == 'POST':
  form = MammogramExamForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('exams.view') 
 return render(request, 'form.html', {'form': form})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def store(request):
    if request.method == 'POST':
        form = MammogramExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user_ip = get_client_ip(request)
            exam.save()
            return redirect('exams.view')

    return redirect('exams.create')

def edit(request, id):
   exams = get_object_or_404(MammogramExam, pk=id)
   form = MammogramExamForm(instance=exams)
   if request.method == "POST":
    form = MammogramExamForm(request.POST, instance=exams)
    if form.is_valid():
     form.save()
     return redirect('exams.view')
   return render(request, 'instedit.html', {'form': form, 'exams': exams})

def delete(request, id):
    exams = get_object_or_404(MammogramExam, pk=id)
    exams.delete()
    return redirect('exams.view')
from django import forms
from .models import MammogramExam

class MammogramExamForm(forms.ModelForm):
    class Meta:
        model = MammogramExam
        fields = '__all__'
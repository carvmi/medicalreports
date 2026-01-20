from django import forms
from .models import MammogramExam, MammogramImage

class MammogramExamForm(forms.ModelForm):
    class Meta:
        model = MammogramExam
        fields = '__all__'

class MammogramImageForm(forms.ModelForm):
    class Meta:
        model = MammogramImage
        fields = '__all__'
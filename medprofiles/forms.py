from django import forms
from .models import HealthProfessional

class MedForm(forms.ModelForm):
    class Meta:
        model = HealthProfessional
        fields = '__all__'
from django import forms
from .models import Institution

class InstForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'
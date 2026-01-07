from django import forms
from .models import Institution

class InstForm(forms.InstForm):
    class Meta:
        model = Institution
        fields = '__all__'
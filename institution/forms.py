from django import forms
from .models import Institution, Address

class InstForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

from django import forms
from .models import Institution, Address

class InstForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                "class",
                "w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 "
                "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100",
            )

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                "class",
                "w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 "
                "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100",
            )

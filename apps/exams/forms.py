from django import forms
from .models import MammogramExam
from apps.patients.models import Patient
from apps.institution.models import Institution

class MammogramExamForm(forms.ModelForm):
    class Meta:
        model = MammogramExam
        exclude = ("is_active", "deleted_at", "user_ip")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["patient"].queryset = Patient.objects.filter(is_active=True)
        self.fields["local"].queryset = Institution.objects.filter(is_active=True)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                "class",
                "w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 "
                "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100",
            )

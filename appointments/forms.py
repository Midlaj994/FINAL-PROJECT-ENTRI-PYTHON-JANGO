from django import forms
from django.contrib.auth import get_user_model

from .models import Appointment

User = get_user_model()


class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.Roles.DOCTOR).order_by("first_name", "last_name"),
        widget=forms.Select(attrs={"class": "form-select"}),
        empty_label="-- choose a doctor --",
        required=True,
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    reason = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Appointment
        fields = ["doctor", "date", "reason"]


class AppointmentNotesForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
        }

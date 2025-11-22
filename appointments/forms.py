from django import forms
from django.contrib.auth import get_user_model

from .models import Appointment

User = get_user_model()


class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.none(),
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

    def __init__(self, *args, specialty_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["doctor"].queryset = User.objects.none()

        if specialty_id:
            self.fields["doctor"].queryset = User.objects.filter(
                role=User.Roles.DOCTOR,
                doctor_profile__specialty_id=specialty_id,
            ).order_by("first_name", "last_name")
            return

        if self.is_bound:
            posted_specialty_id = self.data.get("specialty_id")
            if posted_specialty_id:
                self.fields["doctor"].queryset = User.objects.filter(
                    role=User.Roles.DOCTOR,
                    doctor_profile__specialty_id=posted_specialty_id,
                ).order_by("first_name", "last_name")
            else:
                self.fields["doctor"].queryset = User.objects.filter(
                    role=User.Roles.DOCTOR
                ).order_by("first_name", "last_name")


class AppointmentNotesForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "class": "form-control",
                "placeholder": "Doctor notes (visible only to you)",
            }
        ),
        required=False,
    )

    class Meta:
        model = Appointment
        fields = ["notes"]

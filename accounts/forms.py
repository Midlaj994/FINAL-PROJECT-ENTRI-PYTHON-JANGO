from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from .models import Doctor, Specialty

User = get_user_model()

class PatientSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.PATIENT
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AdminSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.ADMIN
        user.is_staff = True
        user.is_superuser = False
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class AdminAddDoctorForm(forms.Form):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={"class":"form-control form-control-sm"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control form-control-sm"}), required=True)
    first_name = forms.CharField(label="First name", required=False, widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}))
    last_name = forms.CharField(label="Last name", required=False, widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}))
    specialty = forms.ModelChoiceField(label="Specialty", queryset=Specialty.objects.all(), required=True, widget=forms.Select(attrs={"class":"form-select form-select-sm"}))

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self):
        data = self.cleaned_data
        email = data["email"]
        password = data["password"]
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        specialty = data["specialty"]

        create_user = getattr(User.objects, "create_user", None)
        if callable(create_user):
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        else:
            user = User(username=email, email=email, first_name=first_name, last_name=last_name, is_active=True)
            user.set_password(password)
            user.save()

        try:
            user.role = User.Roles.DOCTOR
        except Exception:
            user.role = "DOCTOR"
        user.save()

        doctor = Doctor.objects.create(user=user, specialty=specialty)
        return doctor

class SpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "e.g. Oncology Pediatrics"})
        }

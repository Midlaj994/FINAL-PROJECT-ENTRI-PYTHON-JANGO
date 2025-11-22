# accounts/urls.py

from django.urls import path
from .views import CustomLoginView, signup_patient, signup_doctor, signup_admin, logout_view, doctors_by_specialty, admin_remove_user

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/patient/", views.signup_patient, name="signup_patient"),
    path("signup/doctor/", views.signup_doctor, name="signup_doctor"),
    path("signup/admin/", views.signup_admin, name="signup_admin"),
    path("admin/remove_user/", admin_remove_user, name="admin_remove_user"),

    path("ajax/doctors_by_specialty/", views.doctors_by_specialty, name="doctors_by_specialty"),
]

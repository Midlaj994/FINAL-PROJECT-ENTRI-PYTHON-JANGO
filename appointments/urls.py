from django.urls import path
from .views import patient_book, doctor_upcoming, admin_dashboard, admin_confirm, admin_cancel, doctor_notes


urlpatterns = [
    path("book/", patient_book, name="patient_book"),
    path("doctor/upcoming/", doctor_upcoming, name="doctor_upcoming"),
    path("doctor/appointments/<int:pk>/notes/", doctor_notes, name="doctor_notes"),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/confirm/<int:pk>/", admin_confirm, name="admin_confirm"),
    path("admin/cancel/<int:pk>/", admin_cancel, name="admin_cancel"),
]
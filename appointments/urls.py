from django.urls import path

from .views import (
    patient_book,
    doctor_upcoming,
    doctor_notes,
    admin_dashboard,
    admin_confirm,
    admin_cancel,
)

urlpatterns = [
    path("book/", patient_book, name="patient_book"),
    path("doctor/", doctor_upcoming, name="doctor_upcoming"),
    path("doctor/notes/<int:pk>/", doctor_notes, name="doctor_notes"),
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path("admin/confirm/<int:pk>/", admin_confirm, name="admin_confirm"),
    path("admin/cancel/<int:pk>/", admin_cancel, name="admin_cancel"),
]

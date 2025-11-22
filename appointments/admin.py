from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("date", "patient", "doctor", "status", "created_at")
    list_filter = ("status", "date", "doctor")
    search_fields = ("patient__username", "doctor__username", "reason")
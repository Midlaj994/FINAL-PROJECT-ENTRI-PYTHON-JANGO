from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Doctor, Patient, Specialty

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "email")


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("user_email", "user_fullname", "specialty")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("specialty",)

    def user_email(self, obj):
        return obj.user.email

    def user_fullname(self, obj):
        return obj.user.get_full_name() or obj.user.username


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("user_email", "user_fullname", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("is_active",)

    def user_email(self, obj):
        return obj.user.email

    def user_fullname(self, obj):
        return obj.user.get_full_name() or obj.user.username

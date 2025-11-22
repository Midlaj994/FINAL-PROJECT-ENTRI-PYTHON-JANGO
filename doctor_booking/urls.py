from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Keep admin available for development, but we won't use it for the custom admin panel.
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("appointments/", include(("appointments.urls", "appointments"), namespace="appointments")),
]
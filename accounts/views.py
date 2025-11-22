from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST



from .forms import (
    PatientSignUpForm,
    AdminSignUpForm,
    LoginForm,
)

from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()


def role_required(role):
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("accounts:login")
            if request.user.role != role:
                messages.error(request, "You do not have permission to access this page.")
                return redirect("home")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


def signup_patient(request):
    if request.method == "POST":
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(
                subject="Welcome !!",
                message="Welcome! Your account has been created.",
                from_email=None,
                recipient_list=[user.email] if user.email else [],
                fail_silently=True,
            )
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("home")
    else:
        form = PatientSignUpForm()
    return render(request, "accounts/signup_patient.html", {"form": form})


def signup_doctor(request):
    messages.info(request, "Dear Doctor self-signup is disabled. Please contact the administrator.")
    return redirect("accounts:login")


@role_required(User.Roles.ADMIN)
def signup_admin(request):
    if request.method == "POST":
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin user created.")
            return redirect(reverse("appointments:admin_dashboard"))
    else:
        form = AdminSignUpForm()
    return render(request, "accounts/signup_admin.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


@require_GET
def doctors_by_specialty(request):
    specialty_id = request.GET.get("specialty_id")
    if not specialty_id:
        return JsonResponse({"error": "specialty_id parameter required"}, status=400)
    try:
        specialty_pk = int(specialty_id)
    except (TypeError, ValueError):
        return JsonResponse({"error": "specialty_id must be an integer"}, status=400)

    qs = Doctor.objects.filter(specialty_id=specialty_pk).select_related("user").order_by("user__first_name", "user__last_name")

    doctors = [
        {
            "id": d.user.pk,
            "name": d.user.get_full_name() or d.user.username,
            "email": d.user.email,
        }
        for d in qs
    ]
    return JsonResponse({"doctors": doctors})



@require_POST
@role_required(User.Roles.ADMIN)
def admin_remove_user(request):
    user_id = request.POST.get("user_id")
    if not user_id:
        messages.error(request, "Missing user id.")
        return redirect(reverse("appointments:admin_dashboard"))

    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        messages.error(request, "Invalid user id.")
        return redirect(reverse("appointments:admin_dashboard"))

    if request.user.pk == uid:
        messages.error(request, "You cannot delete your own admin account.")
        return redirect(reverse("appointments:admin_dashboard"))

    target = get_object_or_404(User, pk=uid)

    if target.is_superuser:
        messages.error(request, "Cannot delete a superuser account.")
        return redirect(reverse("appointments:admin_dashboard"))

    # Remove related profiles if exist
    try:
        from .models import Doctor, Patient
        Doctor.objects.filter(user=target).delete()
    except Exception:
        pass
    try:
        from .models import Patient
        Patient.objects.filter(user=target).delete()
    except Exception:
        pass

    email = target.email or target.username
    target.delete()

    messages.success(request, f"User {email} removed.")
    return redirect(reverse("appointments:admin_dashboard"))
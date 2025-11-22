from datetime import date as date_cls

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Appointment
from .forms import AppointmentForm, AppointmentNotesForm
from accounts.models import Doctor, Patient, Specialty
from accounts.forms import AdminAddDoctorForm, SpecialtyForm

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


@role_required(User.Roles.PATIENT)
def patient_book(request):
    preselected_specialty_id = request.GET.get("specialty_id")
    try:
        preselected_specialty_id = int(preselected_specialty_id) if preselected_specialty_id else None
    except (TypeError, ValueError):
        preselected_specialty_id = None

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = request.user
            appt.status = Appointment.Status.PENDING
            appt.save()

            if request.user.email:
                send_mail(
                    subject="Appointment Booking In review",
                    message=f"Your appointment on {appt.date} for reason '{appt.reason}' "
                            f"has been submitted and is pending confirmation.",
                    from_email=None,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )

            messages.success(request, "Appointment submitted and is pending confirmation.")
            return redirect("home")
    else:
        form = AppointmentForm(specialty_id=preselected_specialty_id)

    specialties = Specialty.objects.all().order_by("name")
    context = {
        "form": form,
        "specialties": specialties,
    }
    return render(request, "appointments/patient_book.html", context)


@role_required(User.Roles.DOCTOR)
def doctor_upcoming(request):
    today = date_cls.today()

    upcoming = Appointment.objects.filter(
        doctor=request.user,
        status=Appointment.Status.CONFIRMED,
        date__gte=today,
    ).order_by("date")

    past = Appointment.objects.filter(
        doctor=request.user,
        status=Appointment.Status.CONFIRMED,
        date__lt=today,
    ).order_by("-date")

    context = {
        "upcoming_appointments": upcoming,
        "past_appointments": past,
    }
    return render(request, "appointments/doctor_upcoming.html", context)


@role_required(User.Roles.DOCTOR)
def doctor_notes(request, pk):
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        doctor=request.user,
    )

    if request.method == "POST":
        form = AppointmentNotesForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Notes saved.")
            return redirect("appointments:doctor_upcoming")
    else:
        form = AppointmentNotesForm(instance=appointment)

    context = {
        "appointment": appointment,
        "form": form,
    }
    return render(request, "appointments/doctor_notes.html", context)


@role_required(User.Roles.ADMIN)
def admin_confirm(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = Appointment.Status.CONFIRMED
    appt.save()

    if appt.patient.email:
        send_mail(
            subject="Appointment Confirmed",
            message=f"Your appointment on {appt.date} for reason '{appt.reason}' "
                    f"has been confirmed.",
            from_email=None,
            recipient_list=[appt.patient.email],
            fail_silently=True,
        )

    messages.success(request, "Appointment confirmed.")
    return redirect(reverse("appointments:admin_dashboard"))


@role_required(User.Roles.ADMIN)
def admin_cancel(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = Appointment.Status.CANCELLED
    appt.save()

    if appt.patient.email:
        send_mail(
            subject="Appointment Cancelled",
            message=f"Your appointment on {appt.date} for reason '{appt.reason}' "
                    f"has been cancelled.",
            from_email=None,
            recipient_list=[appt.patient.email],
            fail_silently=True,
        )

    messages.info(request, "Appointment cancelled.")
    return redirect(reverse("appointments:admin_dashboard"))


@role_required(User.Roles.ADMIN)
def admin_dashboard(request):
    pending = Appointment.objects.filter(
        status=Appointment.Status.PENDING
    ).order_by("date")
    confirmed = Appointment.objects.filter(
        status=Appointment.Status.CONFIRMED
    ).order_by("date")
    cancelled = Appointment.objects.filter(
        status=Appointment.Status.CANCELLED
    ).order_by("-date")

    doctors = Doctor.objects.select_related("user", "specialty").order_by(
        "user__first_name", "user__last_name"
    )
    patients = Patient.objects.select_related("user").order_by("-created_at")

    add_doctor_form = AdminAddDoctorForm()
    add_specialty_form = SpecialtyForm()

    if request.method == "POST" and request.POST.get("action") == "add_doctor":
        add_doctor_form = AdminAddDoctorForm(request.POST)
        if add_doctor_form.is_valid():
            add_doctor_form.save()
            messages.success(request, "Doctor account created successfully.")
            return redirect(reverse("appointments:admin_dashboard"))
        messages.error(request, "Please fix the errors in the doctor form.")

    if request.method == "POST" and request.POST.get("action") == "add_specialty":
        add_specialty_form = SpecialtyForm(request.POST)
        if add_specialty_form.is_valid():
            add_specialty_form.save()
            messages.success(request, "Specialty created successfully.")
            return redirect(reverse("appointments:admin_dashboard"))
        messages.error(request, "Please fix the errors in the specialty form.")
    
    specialties = Specialty.objects.all().order_by("name")

    context = {
        "pending": pending,
        "confirmed": confirmed,
        "cancelled": cancelled,
        "doctors": doctors,
        "patients": patients,
        "add_doctor_form": add_doctor_form,
        "add_specialty_form": add_specialty_form,
        "specialties": specialties,
    }
    return render(request, "appointments/admin_dashboard.html", context)

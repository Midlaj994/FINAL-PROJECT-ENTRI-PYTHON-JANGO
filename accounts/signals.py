from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Doctor, Patient

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return


    if instance.role == User.Roles.PATIENT:
        Patient.objects.get_or_create(user=instance)


    if instance.role == User.Roles.DOCTOR:
        Doctor.objects.get_or_create(user=instance)

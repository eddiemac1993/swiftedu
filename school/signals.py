# signals.py
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import UserActivityLog, User  # Import your custom User model

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action="Logged in",
        details=f"IP: {request.META.get('REMOTE_ADDR')}"
    )
    
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action="Logged out",
        details=f"IP: {request.META.get('REMOTE_ADDR')}"
    )
    
@receiver(post_save, sender=User)
def log_profile_update(sender, instance, created, **kwargs):
    if not created:  # Only log updates, not creations
        UserActivityLog.objects.create(
            user=instance,
            action="Updated profile",
            details=f"Updated user: {instance.email}"
        )
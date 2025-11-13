"""
Signals for automatic notifications
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .services import NotificationService

User = get_user_model()


# Note: Welcome email is sent from RegisterView to have better control
# Uncomment this if you want automatic welcome emails via signals instead
# @receiver(post_save, sender=User)
# def send_welcome_email_on_user_creation(sender, instance, created, **kwargs):
#     """
#     Automatically send welcome email when a new user is created
#     """
#     if created and instance.email:
#         # Send welcome email asynchronously (you can use Celery for this in production)
#         NotificationService.send_welcome_email(instance)


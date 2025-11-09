import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(unique=True, max_length=15, blank=False, null=False)

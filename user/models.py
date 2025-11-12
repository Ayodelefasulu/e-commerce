import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    email = models.EmailField(unique=True, blank=False, null=False, db_index=True)
    phone_number = models.CharField(unique=True, max_length=15, blank=False, null=False, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['uuid']),
            models.Index(fields=['username']),
        ]

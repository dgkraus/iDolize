from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        profile_id = self.id

        super().save(*args,**kwargs)
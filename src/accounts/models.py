from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class AccountDeleteCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.username} - {self.code}"

class User(AbstractUser):
    ROLE_CHOICES = [
        ('satici', 'Satıcı'),
        ('musteri', 'Müşteri'),
        ('yonetici', 'Yönetici'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    tc_kimlik = models.CharField(max_length=11, unique=True)
# Create your models here.

    REQUIRED_FIELDS = ['tc_kimlik', 'role'] + [f for f in AbstractUser.REQUIRED_FIELDS if f != 'email']

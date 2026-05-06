from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('satici', 'Satıcı'),
        ('musteri', 'Müşteri'),
        ('yonetici', 'Yönetici'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    tc_kimlik = models.CharField(max_length=11, unique=True)
# Create your models here.

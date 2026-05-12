from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name='Kullanici',
    )
    bakiye = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('10000.00'),
        verbose_name='Sahte Para Bakiyesi',
    )
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cuzdan'
        verbose_name_plural = 'Cuzdanlar'

    def __str__(self):
        return f"{self.user} - {self.bakiye} TL"

    def clean(self):
        if self.bakiye < 0:
            raise ValidationError({'bakiye': 'Bakiye negatif olamaz.'})




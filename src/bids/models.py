from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class BidIncrement(models.Model):
    
    auction = models.OneToOneField(
        'auction.Auction',
        on_delete=models.CASCADE,
        related_name='teklif_ayari',
        verbose_name="Muzayede",
    )
    artis_adimi = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        verbose_name="Artis Adimi",
        help_text="Yeni teklif, mevcut fiyatin en az bu miktar kadar uzerinde olmalidir.",
    )
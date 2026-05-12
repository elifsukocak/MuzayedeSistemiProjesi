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
    
    class Meta:
        verbose_name = "Teklif Artis Ayari"
        verbose_name_plural = "Teklif Artis Ayarlari"

    def clean(self):
        if self.artis_adimi <= 0:
            raise ValidationError({"artis_adimi": "Artis adimi 0'dan buyuk olmalidir."})

    def __str__(self):
        return f"{self.auction} - {self.artis_adimi} TL"


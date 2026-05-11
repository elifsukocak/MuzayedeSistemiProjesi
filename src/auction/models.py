from django.conf import settings
from django.db import models
from django.utils import timezone

from products.models import Urun


class Auction(models.Model):
    product = models.OneToOneField(
        Urun,
        on_delete=models.CASCADE,
        related_name='auction',
        limit_choices_to={'durum': 'aktif'},
    )
    baslangic_zamani = models.DateTimeField(default=timezone.now)
    bitis_zamani = models.DateTimeField()
    mevcut_fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    kazanan = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kazanilan_muzayedeler',
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Muzayede"
        verbose_name_plural = "Muzayedeler"

    def __str__(self):
        return f"{self.product.ad} - {self.mevcut_fiyat} TL"

    def sure_doldu_mu(self):
        return timezone.now() >= self.bitis_zamani

    def kalan_gun(self):
        if not self.is_active:
            return 0
        kalan = self.bitis_zamani - timezone.now()
        return max(kalan.days + (1 if kalan.seconds else 0), 0)

    def check_and_close(self):
        if self.sure_doldu_mu() and self.is_active:
            return self.close_auction()
        return False

    def close_auction(self):
        if not self.is_active:
            return False

        from bids.models import Bid, BidStatusNotification
        from pays.services import transfer_auction_payment

        self.is_active = False
        winner_bid = Bid.objects.filter(auction=self, durum='GECERLI').order_by('-miktar').first()

        if winner_bid:
            self.kazanan = winner_bid.kullanici
            self.product.durum = 'satildi'
            transfer_auction_payment(winner_bid.kullanici, self.product.satici, winner_bid.miktar)
            BidStatusNotification.objects.create(
                kullanici=winner_bid.kullanici,
                bid=winner_bid,
                mesaj=f"{self.product.ad} muzayedesini {winner_bid.miktar} TL ile kazandiniz.",
            )
            BidStatusNotification.objects.create(
                kullanici=self.product.satici,
                bid=winner_bid,
                mesaj=f"{self.product.ad} satildi. {winner_bid.miktar} TL bakiyenize aktarildi.",
            )
        else:
            self.product.durum = 'suresi_doldu'

        self.product.save()
        self.save()
        return True

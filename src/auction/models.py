from django.db import models
from products.models import Urun
from django.utils import timezone
from django.conf import settings


class Auction(models.Model):
    # Rapor: "Her ürün yalnızca bir müzayedeye sahiptir (1-1 ilişki)"
    product = models.OneToOneField(
        Urun,
        on_delete=models.CASCADE,
        related_name='auction',
        limit_choices_to={'durum': 'aktif'}  # Sadece aktif ürünler müzayede olabilir
    )

    # Rapor: "Müzayede ve Teklif Verileri"
    baslangic_zamani = models.DateTimeField(default=timezone.now)
    bitis_zamani = models.DateTimeField()

    # Rapor: "Mevcut en yüksek fiyat"
    mevcut_fiyat = models.DecimalField(max_digits=10, decimal_places=2)

    # Rapor: "En yüksek teklifi veren müşteri"
    kazanan = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kazanilan_muzayedeler'
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Müzayede"
        verbose_name_plural = "Müzayedeler"

    def __str__(self):
        return f"{self.product.ad} - {self.mevcut_fiyat} TL"

    # Rapor: "sureKontrol()" metodu
    def sure_doldu_mu(self):
        return timezone.now() >= self.bitis_zamani

    def check_and_close(self):
        """Müzayede süresini kontrol eder ve gerekiyorsa kapatır."""
        if self.sure_doldu_mu() and self.is_active:
            self.is_active = False  # Müzayedeyi pasif yap

            # En yüksek geçerli teklifi bul
            # 'bids' app'indeki Bid modelini burada import etmen gerekebilir
            from bids.models import Bid
            winner_bid = Bid.objects.filter(auction=self, durum='GECERLI').order_by('-miktar').first()

            if winner_bid:
                self.kazanan = winner_bid.kullanici  # En yüksek teklif veren kazanan olur
                self.product.durum = 'satildi'  # Ürün durumunu güncelle
                #komisyon = winner_bid.miktar * (self.yonetici_komisyon_orani / 100)
            else:
                self.product.durum = 'suresi_doldu'  # Teklif yoksa süre doldu

            self.product.save()  # Ürün tablosunu kaydet
            self.save()  # Müzayede tablosunu kaydet
            return True
        return False
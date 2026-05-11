from django.db import models
from django.conf import settings

class Kategori (models.Model):
    ad = models.CharField(max_length=100, verbose_name="Kategori Adı")
    ust_kategori = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Üst Kategori"
    )

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        if self.ust_kategori:
            return f"{self.ust_kategori.ad} -> {self.ad}"
        return self.ad

class Urun (models.Model):
    DURUM_SECENEKLERI = [
        ('taslak', 'Taslak'),
        ('onay_bekliyor', 'Onay Bekliyor'),
        ('aktif', 'Aktif'),
        ('satildi', 'Satıldı'),
        ('reddedildi', 'Reddedildi'),
        ('suresi_doldu', 'Süresi Doldu'),
    ]

    satici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='urunler',
                               verbose_name="Satıcı")
    ad = models.CharField(max_length=200, verbose_name="Ürün Adı")
    aciklama = models.TextField(verbose_name="Açıklama")
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True, related_name='urunler',
                                 verbose_name="Kategori")
    baslangicFiyati = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Başlangıç Fiyatı")
    artis_adimi = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        verbose_name="Artış Adımı",
        help_text="Tekliflerin kaç TL aralıklarla artacağını belirler.",
    )
    teklif_suresi_gun = models.PositiveIntegerField(
        default=7,
        verbose_name="Teklif Süresi (Gün)",
        help_text="Ürün onaylandıktan sonra müzayedenin kaç gün açık kalacağı.",
    )
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='onay_bekliyor', verbose_name="Durum")
    red_sebebi = models.TextField(verbose_name="Reddedilme Sebebi", blank=True, null=True,
                                  help_text="Eğer ürün reddedilirse, satıcıya gösterilecek sebep.")

    # Ekstra gerekli alanlar (Tasarıma zarar vermeyen zorunlu web alanları)
    gorsel = models.ImageField(upload_to='urun_gorselleri/', null=True, blank=True, verbose_name="Görsel")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    def __str__(self):
        return self.ad

    def get_durum_renk(self):
        from django.utils.html import format_html
        renkler = {
            'taslak': 'gray',
            'onay_bekliyor': 'orange',
            'aktif': 'green',
            'satildi': 'blue',
            'suresi_doldu': 'red',
            'reddedildi': 'black',
        }
        renk = renkler.get(self.durum, 'gray')
        return format_html(
            '<b style="color:{};">{}</b>',
            renk,
            self.get_durum_display()
        )
    get_durum_renk.short_description = "Durum"

from django.contrib import admin
from .models import Kategori, Urun

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('ad', 'ust_kategori')
    search_fields = ('ad',)
    list_filter = ('ust_kategori',)

@admin.register(Urun)
class UrunAdmin(admin.ModelAdmin):
    # Tasarım raporuna göre güncellenen alanlar ve renkli durum fonksiyonu
    list_display = ('ad', 'kategori', 'satici', 'get_durum_renk', 'baslangicFiyati')
    list_filter = ('durum', 'kategori')
    search_fields = ('ad', 'aciklama')
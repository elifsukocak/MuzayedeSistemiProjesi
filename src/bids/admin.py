from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Bid


@admin.register(Bid)
# Bid modelini admin paneline kaydet
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'kullanici', 'miktar', 'durum', 'zaman')
    list_filter = ('durum', 'zaman')
    search_fields = ('auction__product__ad', 'kullanici__username')
    readonly_fields = ('zaman',)
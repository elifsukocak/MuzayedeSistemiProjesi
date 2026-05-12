from django.contrib import admin

from .models import Bid, BidIncrement, BidStatusNotification


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'kullanici', 'miktar', 'durum', 'zaman')
    list_filter = ('durum', 'zaman')
    search_fields = ('auction__product__ad', 'kullanici__username')
    readonly_fields = ('zaman',)


@admin.register(BidIncrement)
class BidIncrementAdmin(admin.ModelAdmin):
    list_display = ('auction', 'artis_adimi')
    search_fields = ('auction__product__ad',)


@admin.register(BidStatusNotification)
class BidStatusNotificationAdmin(admin.ModelAdmin):
    list_display = ('kullanici', 'bid', 'okundu', 'olusturulma_tarihi')
    list_filter = ('okundu', 'olusturulma_tarihi')
    search_fields = ('kullanici__username', 'mesaj')
    readonly_fields = ('olusturulma_tarihi',)

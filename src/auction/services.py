from django.db import transaction
from bids.models import Bid


def place_bid(user, auction, miktar):
    # Eşzamanlılık kontrolü için veritabanını kilitliyoruz[cite: 1]
    with transaction.atomic():
        # Kuralları kontrol et[cite: 2]
        if auction.sure_doldu_mu():
            return "Hata: Müzayede süresi dolmuş."

        if miktar <= auction.mevcut_fiyat:
            return f"Hata: Teklifiniz mevcut fiyattan ({auction.mevcut_fiyat} TL) yüksek olmalı."

        last_bid = Bid.objects.filter(auction=auction).order_by('-zaman').first()
        if last_bid and last_bid.kullanici == user:
            return "Hata: Zaten en yüksek teklif size ait. Üst üste teklif veremezsiniz."

        # Kurallardan geçtiyse eski teklifi geçersiz yapıp yenisini kaydet[cite: 2]
        Bid.objects.filter(auction=auction, durum='GECERLI').update(durum='GECILDI')
        Bid.objects.create(auction=auction, kullanici=user, miktar=miktar, durum='GECERLI')

        auction.mevcut_fiyat = miktar
        auction.save()
        return "Başarılı: Teklifiniz başarıyla alındı!"

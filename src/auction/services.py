from decimal import Decimal, InvalidOperation

from django.db import transaction

from bids.models import Bid, BidIncrement, BidStatusNotification
from pays.services import get_wallet


def place_bid(user, auction, miktar):
    try:
        miktar = Decimal(str(miktar))
    except (InvalidOperation, TypeError):
        return "Hata: Gecerli bir teklif miktari giriniz."

    if not user.is_authenticated:
        return "Hata: Teklif verebilmek icin giris yapmalisiniz."

    if auction.product.satici_id == user.id:
        return "Hata: Kendi urununuze teklif veremezsiniz."

    with transaction.atomic():
        auction = auction.__class__.objects.select_for_update().get(pk=auction.pk)

        if auction.sure_doldu_mu():
            auction.check_and_close()
            return "Hata: Muzayede suresi dolmus."

        if not auction.is_active:
            return "Hata: Muzayede aktif degil."

        wallet = get_wallet(user)
        if wallet.bakiye < miktar:
            return "Hata: Bu teklif icin bakiyeniz yetersiz."

        teklif_ayari, _ = BidIncrement.objects.get_or_create(auction=auction)
        minimum_teklif = auction.mevcut_fiyat + teklif_ayari.artis_adimi
        if miktar < minimum_teklif:
            return f"Hata: Teklifiniz en az {minimum_teklif} TL olmalidir."

        last_bid = Bid.objects.filter(auction=auction, durum='GECERLI').order_by('-zaman').first()
        if last_bid and last_bid.kullanici == user:
            return "Hata: Zaten en yuksek teklif size ait. Ust uste teklif veremezsiniz."

        Bid.objects.filter(auction=auction, durum='GECERLI').update(durum='GECILDI')
        yeni_teklif = Bid.objects.create(auction=auction, kullanici=user, miktar=miktar, durum='GECERLI')

        if last_bid:
            BidStatusNotification.objects.create(
                kullanici=last_bid.kullanici,
                bid=last_bid,
                mesaj=f"{auction.product.ad} urunundeki {last_bid.miktar} TL teklifiniz gecildi.",
            )
        BidStatusNotification.objects.create(
            kullanici=user,
            bid=yeni_teklif,
            mesaj=f"{auction.product.ad} urununde {miktar} TL teklifiniz aktif.",
        )

        auction.mevcut_fiyat = miktar
        auction.kazanan = user
        auction.save()
        return "Basarili: Teklifiniz aktif teklif olarak kaydedildi."

from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from auction.models import Auction
from auction.services import place_bid
from .models import Bid, BidIncrement, BidStatusNotification

@login_required
def teklif_ver(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    if request.method != 'POST':
        return redirect('auction_detail', id=auction.id)

    miktar = request.POST.get('miktar')
    mesaj = place_bid(request.user, auction, miktar)
    if mesaj.startswith('Basarili'):
        messages.success(request, mesaj)
    else:
        messages.error(request, mesaj)

    return redirect('auction_detail', id=auction.id)

@login_required
def artis_adimi_guncelle(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    if auction.product.satici_id != request.user.id:
        messages.error(request, "Bu muzayedenin artis adimini sadece urunun saticisi guncelleyebilir.")
        return redirect('auction_detail', id=auction.id)

    teklif_ayari, _ = BidIncrement.objects.get_or_create(auction=auction)

    if request.method == 'POST':
        try:
            artis_adimi = Decimal(str(request.POST.get('artis_adimi')))
        except (InvalidOperation, TypeError):
            messages.error(request, "Gecerli bir artis adimi giriniz.")
            return redirect('bids:artis_adimi_guncelle', auction_id=auction.id)

        teklif_ayari.artis_adimi = artis_adimi
        try:
            teklif_ayari.full_clean()
        except Exception as exc:
            messages.error(request, exc)
        else:
            teklif_ayari.save()
            messages.success(request, "Artis adimi guncellendi.")
            return redirect('auction_detail', id=auction.id)

    return render(request, 'bids/artis_adimi_form.html', {'auction': auction, 'teklif_ayari': teklif_ayari})

@login_required
def tekliflerim(request):
    teklifler = Bid.objects.filter(kullanici=request.user).select_related('auction', 'auction__product')
    bildirimler = BidStatusNotification.objects.filter(kullanici=request.user).select_related('bid', 'bid__auction')
    return render(request, 'bids/tekliflerim.html', {'teklifler': teklifler, 'bildirimler': bildirimler})

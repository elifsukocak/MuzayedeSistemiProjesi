from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from bids.models import Bid
from .models import Auction
from .services import place_bid


def auction_list(request):
    active_auctions = Auction.objects.filter(is_active=True)
    for auction in active_auctions:
        auction.check_and_close()

    auctions = Auction.objects.filter(is_active=True)
    return render(request, 'auction/list.html', {'auctions': auctions})


def auction_detail(request, id):
    auction = get_object_or_404(Auction, id=id)
    auction.check_and_close()
    auction.refresh_from_db()
    teklifler = Bid.objects.filter(auction=auction).order_by('-miktar')
    teklif_ayari = getattr(auction, 'teklif_ayari', None)
    minimum_teklif = None
    if auction.is_active:
        artis_adimi = teklif_ayari.artis_adimi if teklif_ayari else Decimal('1.00')
        minimum_teklif = auction.mevcut_fiyat + artis_adimi
    return render(request, "auction/detail.html", {
        "auction": auction,
        "teklifler": teklifler,
        "teklif_ayari": teklif_ayari,
        "minimum_teklif": minimum_teklif,
    })


@login_required
def bid_view(request, id):
    auction = get_object_or_404(Auction, id=id)

    if request.method == "POST":
        mesaj = place_bid(request.user, auction, request.POST.get("miktar"))
        messages.info(request, mesaj)

    return redirect("auction_detail", id=id)


@login_required
def auction_close(request, id):
    auction = get_object_or_404(Auction, id=id)
    if auction.product.satici_id != request.user.id:
        messages.error(request, "Bu muzayedeyi sadece urunun saticisi sonlandirabilir.")
        return redirect("auction_detail", id=id)

    if request.method == "POST":
        if auction.close_auction():
            messages.success(request, "Muzayede sonlandirildi ve kazanan belirlendi.")
        else:
            messages.info(request, "Muzayede zaten kapali.")

    return redirect("auction_detail", id=id)

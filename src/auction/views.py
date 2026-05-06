from django.shortcuts import render, get_object_or_404, redirect
from .models import Auction
from .services import place_bid
from django.contrib import messages
from bids.models import Bid


def auction_list(request):
    # ÖNCE: Tüm aktif müzayedeleri çek ve sürelerini kontrol et
    active_auctions = Auction.objects.filter(is_active=True)
    for auction in active_auctions:
        auction.check_and_close()  # Süresi dolanlar burada otomatik kapanır

    # SONRA: Güncel (hala aktif olan) müzayedeleri kullanıcıya göster
    auctions = Auction.objects.filter(is_active=True)
    return render(request, 'auction/list.html', {'auctions': auctions})


def auction_detail(request, id):
    auction = get_object_or_404(Auction, id=id)

    # Müzayedeye ait teklifleri yüksekten düşüğe (veya en yeniden eskiye) sırala
    teklifler = Bid.objects.filter(auction=auction).order_by('-miktar')

    # context içine teklifler'i de ekliyoruz
    return render(request, "auction/detail.html", {"auction": auction, "teklifler": teklifler})


def bid_view(request, id):
    auction = get_object_or_404(Auction, id=id)

    if request.method == "POST":
        miktar = float(request.POST.get("miktar"))
        mesaj = place_bid(request.user, auction, miktar)
        messages.info(request, mesaj)  # şimdilik terminalde gör

    return redirect("auction_detail", id=id)
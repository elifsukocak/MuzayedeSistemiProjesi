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

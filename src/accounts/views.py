from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from bids.models import Bid, BidStatusNotification
from pays.services import get_wallet
from products.models import Urun

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == "yonetici":
                return redirect("products:yonetici_onay_listesi")

            elif user.role == "satici":
                return redirect("products:urunlerimi_listele")

            elif user.role == "musteri":
                return redirect("bids:tekliflerim")

            else:
                return redirect("profile")

        else:
            return render(request, "accounts/login.html", {
                "error": "Kullanıcı adı veya şifre hatalı"
            })

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    teklifler = Bid.objects.filter(kullanici=request.user)
    urunler = Urun.objects.filter(satici=request.user)
    bildirimler = BidStatusNotification.objects.filter(
        kullanici=request.user,
    ).select_related('bid', 'bid__auction', 'bid__auction__product')[:10]
    okunmamis_bildirimler = BidStatusNotification.objects.filter(
        kullanici=request.user,
        okundu=False,
    )
    okunmamis_bildirim_sayisi = okunmamis_bildirimler.count()
    wallet = get_wallet(request.user)

    okunmamis_bildirimler.update(okundu=True)

    return render(request, "accounts/profile.html", {
        "teklif_sayisi": teklifler.count(),
        "aktif_teklif_sayisi": teklifler.filter(durum='GECERLI').count(),
        "urun_sayisi": urunler.count(),
        "okunmamis_bildirim_sayisi": okunmamis_bildirim_sayisi,
        "bildirimler": bildirimler,
        "wallet": wallet,
    })

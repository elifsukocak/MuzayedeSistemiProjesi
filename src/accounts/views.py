from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
<<<<<<< Updated upstream
=======
@login_required
def hesap_silme_kodu_gonder(request):
    if not request.user.email:
        messages.error(request, "E-posta adresiniz olmadığı için hesap silme kodu gönderilemedi.")
        return redirect("profile")

    code = str(random.randint(1000, 9999))

    AccountDeleteCode.objects.update_or_create(
        user=request.user,
        defaults={"code": code}
    )

    try:
        send_mail(
            "BidLance Hesap Silme Kodu",
            f"Hesabınızı pasifleştirmek için doğrulama kodunuz: {code}",
            None,
            [request.user.email],
            fail_silently=False,
        )
        messages.success(request, "Hesap silme kodu e-posta adresinize gönderildi.")
    except Exception:
        messages.error(request, "Kod gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

    return redirect("hesap_silme_onay")


@login_required
def hesap_silme_onay(request):
    if request.method == "POST":
        girilen_kod = request.POST.get("code")

        try:
            kayit = AccountDeleteCode.objects.get(user=request.user)
        except AccountDeleteCode.DoesNotExist:
            return render(request, "accounts/hesap_silme_onay.html", {
                "error": "Önce doğrulama kodu almalısınız."
            })
        if kayit.is_expired():
            kayit.delete()
            return render(request, "accounts/hesap_silme_onay.html", {
            "error": "Kodun süresi dolmuş. Lütfen yeniden kod alın."
            })
        if kayit.code == girilen_kod:
            user = request.user
            user.is_active = False
            user.save()
            kayit.delete()
            logout(request)
            return redirect("login")

        return render(request, "accounts/hesap_silme_onay.html", {
            "error": "Kod hatalı."
        })

    return render(request, "accounts/hesap_silme_onay.html")
>>>>>>> Stashed changes

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from auction.models import Auction
from bids.models import BidIncrement
from .forms import UrunEkleForm, UrunGuncelleForm
from .models import Urun, Kategori


def yonetici_mi(user):
    return user.is_authenticated and (user.role == 'yonetici' or user.is_staff)

# --- Musteri Islemleri ---

def urun_kategori_incele(request, kategori_id=None):
    for auction in Auction.objects.filter(is_active=True):
        auction.check_and_close()

    urunler = Urun.objects.filter(durum='aktif').order_by('-olusturulma_tarihi')
    kategoriler = Kategori.objects.filter(ust_kategori__isnull=True)
    secili_kategori = None

    #Arama
    arama_kelimesi = request.GET.get('q')
    if arama_kelimesi:
        urunler = urunler.filter(ad__icontains=arama_kelimesi)

    #Kategori Filtreleme
    if kategori_id:
        secili_kategori = get_object_or_404(Kategori, pk=kategori_id)

        gecerli_kategori_idleri = [secili_kategori.id]
        alt_kategoriler = Kategori.objects.filter(ust_kategori=secili_kategori)
        gecerli_kategori_idleri.extend(alt_kategoriler.values_list('id', flat=True))

        urunler = urunler.filter(kategori_id__in=gecerli_kategori_idleri)

    return render(request, 'products/vitrin.html', {
        'urunler': urunler,
        'kategoriler': kategoriler,
        'secili_kategori': secili_kategori,
        'arama_kelimesi': arama_kelimesi,
    })


def urun_detay(request, pk):

    # Urunun detayli bilgilerinin gosterildigi sayfa.

    urun = get_object_or_404(Urun, pk=pk)
    auction = getattr(urun, 'auction', None)
    if auction:
        auction.check_and_close()
        auction.refresh_from_db()
        urun.refresh_from_db()
    teklif_ayari = getattr(auction, 'teklif_ayari', None) if auction else None
    aktif_teklif_var = auction.teklifler.filter(durum='GECERLI').exists() if auction else False
    minimum_teklif = None
    if auction and auction.is_active:
        artis_adimi = teklif_ayari.artis_adimi if teklif_ayari else Decimal('1.00')
        minimum_teklif = auction.mevcut_fiyat + artis_adimi
    return render(request, 'products/detay.html', {
        'urun': urun,
        'auction': auction,
        'teklif_ayari': teklif_ayari,
        'aktif_teklif_var': aktif_teklif_var,
        'minimum_teklif': minimum_teklif,
    })


# --- Satıcı Islemleri ---

@login_required
def urun_ekle(request):
    if request.method == 'POST':
        form = UrunEkleForm(request.POST, request.FILES)
        if form.is_valid():
            yeni_urun = form.save(commit=False)
            yeni_urun.satici = request.user
            yeni_urun.durum = 'onay_bekliyor'
            yeni_urun.save()  # Şimdi kaydet
            return redirect('/urunler/vitrin/')
    else:
        form = UrunEkleForm()

    return render(request, 'products/urun_ekle.html', {'form': form})





@login_required
def urun_guncelle(request, pk):

    # Saticinin henuz muzayedesi baslamamis urunlerini duzenlemesini saglar (UC-05).

    urun = get_object_or_404(Urun, pk=pk)

    if request.method == 'POST':
        form = UrunGuncelleForm(request.POST, request.FILES, instance=urun)
        if form.is_valid():
            guncellenen_urun = form.save(commit=False)

            if guncellenen_urun.durum == 'reddedildi':
                guncellenen_urun.durum = 'onay_bekliyor'
                guncellenen_urun.red_sebebi = ''

                messages.success(request,
                                 f"'{guncellenen_urun.ad}' başarıyla güncellendi ve yeniden yönetici onayına gönderildi! ⏳")
            else:
                # Normal güncelleme mesajı
                messages.success(request, "Ürün başarıyla güncellendi. ✅")

            guncellenen_urun.save()
            return redirect('products:urunlerimi_listele')
    else:
        form = UrunGuncelleForm(instance=urun)

    return render(request, 'products/urun_guncelle.html', {'form': form, 'urun': urun})


def urunlerimi_listele(request):

    # Saticinin kendi ekledigi urunleri durumlariyla birlikte listeledigi panel (UC-06).

    urunler = Urun.objects.filter(satici=request.user)

    return render(request, 'products/urunlerim.html', {'urunler': urunler})


@login_required
@user_passes_test(yonetici_mi)
def yonetici_onay_listesi(request):
    bekleyen_urunler = Urun.objects.filter(durum='onay_bekliyor').select_related('satici', 'kategori')
    reddedilen_urunler = Urun.objects.filter(durum='reddedildi').select_related('satici', 'kategori')[:10]
    return render(request, 'products/yonetici_onay_listesi.html', {
        'bekleyen_urunler': bekleyen_urunler,
        'reddedilen_urunler': reddedilen_urunler,
    })


@login_required
@user_passes_test(yonetici_mi)
def yonetici_urun_onay_detay(request, pk):
    urun = get_object_or_404(Urun.objects.select_related('satici', 'kategori'), pk=pk)

    if request.method == 'POST':
        islem = request.POST.get('islem')

        if islem == 'onayla':
            urun.durum = 'aktif'
            urun.red_sebebi = ''
            urun.save()

            auction, _ = Auction.objects.get_or_create(
                product=urun,
                defaults={
                    'bitis_zamani': timezone.now() + timezone.timedelta(days=urun.teklif_suresi_gun),
                    'mevcut_fiyat': urun.baslangicFiyati,
                    'is_active': True,
                },
            )
            BidIncrement.objects.get_or_create(
                auction=auction,
                defaults={'artis_adimi': urun.artis_adimi},
            )

            messages.success(request, f"'{urun.ad}' onaylandi ve muzayedeye acildi.")
            return redirect('products:yonetici_onay_listesi')

        if islem == 'reddet':
            red_sebebi = request.POST.get('red_sebebi', '').strip()
            if not red_sebebi:
                messages.error(request, "Urunu reddetmek icin red sebebi yazmalisiniz.")
                return redirect('products:yonetici_urun_onay_detay', pk=urun.pk)

            urun.durum = 'reddedildi'
            urun.red_sebebi = red_sebebi
            urun.save()
            messages.warning(request, f"'{urun.ad}' reddedildi.")
            return redirect('products:yonetici_onay_listesi')

    return render(request, 'products/yonetici_urun_onay_detay.html', {'urun': urun})

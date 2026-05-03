from django.shortcuts import render, get_object_or_404, redirect
from .models import Urun, Kategori
from .forms import UrunEkleForm,UrunGuncelleForm
from django.contrib import messages

# --- Musteri Islemleri ---

def urun_kategori_incele(request, kategori_id=None):
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
    return render(request, 'products/detay.html', {'urun': urun})


# --- Satıcı Islemleri ---

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
from django.shortcuts import render, get_object_or_404, redirect
from .models import Urun, Kategori
from .forms import UrunEkleForm,UrunGuncelleForm

# --- Musteri Islemleri ---

def urun_kategori_incele(request, kategori_id=None):
    urunler = Urun.objects.filter(durum='aktif').order_by('-olusturulma_tarihi')
    kategoriler = Kategori.objects.filter(ust_kategori__isnull=True)
    secili_kategori = None

    if kategori_id:
        # slug yerine pk (id) ile arıyoruz
        secili_kategori = get_object_or_404(Kategori, pk=kategori_id)

        gecerli_kategori_idleri = [secili_kategori.id]
        alt_kategoriler = Kategori.objects.filter(ust_kategori=secili_kategori)
        gecerli_kategori_idleri.extend(alt_kategoriler.values_list('id', flat=True))

        urunler = urunler.filter(kategori_id__in=gecerli_kategori_idleri)

    return render(request, 'products/vitrin.html', {
        'urunler': urunler,
        'kategoriler': kategoriler,
        'secili_kategori': secili_kategori
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
    silinebilir_durumlar = ['taslak', 'onay_bekliyor', 'suresi_doldu', 'reddedildi']

    if request.method == 'POST':
        if request.POST.get('islem') == 'sil':
            if urun.durum in silinebilir_durumlar:
                urun.delete()
                return redirect('products:urunlerimi_listele')

        else:
            form = UrunGuncelleForm(request.POST, request.FILES, instance=urun)
            if form.is_valid():
                form.save()
                return redirect('products:urunlerimi_listele')

    else:
        form = UrunGuncelleForm(instance=urun)

    return render(request, 'products/urun_guncelle.html', {'form': form, 'urun': urun})


def urunlerimi_listele(request):

    # Saticinin kendi ekledigi urunleri durumlariyla birlikte listeledigi panel (UC-06).

    urunler = Urun.objects.all()

    return render(request, 'products/urunlerim.html', {'urunler': urunler})
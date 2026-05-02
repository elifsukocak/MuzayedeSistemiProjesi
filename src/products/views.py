from django.shortcuts import render, get_object_or_404, redirect
from .models import Urun, Kategori
from .forms import UrunEkleForm,UrunGuncelleForm

# --- Musteri Islemleri ---

def urun_kategori_incele(request, kategori_slug=None):
    urunler = Urun.objects.filter(durum='aktif').order_by('-olusturulma_tarihi')
    kategoriler = Kategori.objects.all()

    if kategori_slug:
        urunler = urunler.filter(kategori__slug=kategori_slug)

    return render(request, 'products/vitrin.html', {
        'urunler': urunler,
        'kategoriler': kategoriler
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
            form.save()
            return redirect('products:urunlerimi_listele')
    else:
        form = UrunGuncelleForm(instance=urun)

    return render(request, 'products/urun_guncelle.html', {'form': form, 'urun': urun})


def urunlerimi_listele(request):

    # Saticinin kendi ekledigi urunleri durumlariyla birlikte listeledigi panel (UC-06).

    urunler = Urun.objects.all()

    return render(request, 'products/urunlerim.html', {'urunler': urunler})
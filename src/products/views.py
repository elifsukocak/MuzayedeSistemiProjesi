from django.shortcuts import render, get_object_or_404
from .models import Urun, Kategori


# --- Musteri Islemleri ---

def urun_kategori_incele(request, kategori_slug=None):

    # Musterilerin urunleri kategoriye gore filtreleyip inceledigi ana vitrin (UC-07).

    urunler = Urun.objects.filter(durum='aktif')
    kategoriler = Kategori.objects.all()

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

    # Saticinin sisteme yeni bir urun (taslak/onay bekleyen) eklemesini saglar (UC-04).

    return render(request, 'products/urun_ekle.html')


def urun_guncelle(request, pk):

    # Saticinin henuz muzayedesi baslamamis urunlerini duzenlemesini saglar (UC-05).

    urun = get_object_or_404(Urun, pk=pk)
    return render(request, 'products/urun_guncelle.html', {'urun': urun})


def urunlerimi_listele(request):

    # Saticinin kendi ekledigi urunleri durumlariyla birlikte listeledigi panel (UC-06).

    return render(request, 'products/urunlerim.html')
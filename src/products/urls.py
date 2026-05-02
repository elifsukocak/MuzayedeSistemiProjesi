from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Vitrin ve Detay
    path('vitrin/', views.urun_kategori_incele, name='urun_kategori_incele'),
path('vitrin/kategori/<int:kategori_id>/', views.urun_kategori_incele, name='urun_kategori_incele'),    path('urun/<int:pk>/', views.urun_detay, name='urun_detay'),

    # Satici Paneli Islemleri
    path('ekle/', views.urun_ekle, name='urun_ekle'),
    path('guncelle/<int:pk>/', views.urun_guncelle, name='urun_guncelle'),
    path('listem/', views.urunlerimi_listele, name='urunlerimi_listele'),
]
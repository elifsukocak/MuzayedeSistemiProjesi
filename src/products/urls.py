from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('vitrin/', views.urun_kategori_incele, name='urun_kategori_incele'),
    path('vitrin/kategori/<int:kategori_id>/', views.urun_kategori_incele, name='urun_kategori_incele'),
    path('urun/<int:pk>/', views.urun_detay, name='urun_detay'),
    path('ekle/', views.urun_ekle, name='urun_ekle'),
    path('guncelle/<int:pk>/', views.urun_guncelle, name='urun_guncelle'),
    path('listem/', views.urunlerimi_listele, name='urunlerimi_listele'),
    path('yonetici/onaylar/', views.yonetici_onay_listesi, name='yonetici_onay_listesi'),
    path('yonetici/onaylar/<int:pk>/', views.yonetici_urun_onay_detay, name='yonetici_urun_onay_detay'),
]

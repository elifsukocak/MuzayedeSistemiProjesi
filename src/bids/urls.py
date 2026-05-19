from django.urls import path

from . import views

app_name = 'bids'

urlpatterns = [
    path('muzayede/<int:auction_id>/teklif-ver/', views.teklif_ver, name='teklif_ver'),
    path('muzayede/<int:auction_id>/artis-adimi/', views.artis_adimi_guncelle, name='artis_adimi_guncelle'),
    path('tekliflerim/', views.tekliflerim, name='tekliflerim'),
]

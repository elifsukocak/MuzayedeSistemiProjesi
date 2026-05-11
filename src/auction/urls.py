from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('<int:id>/', views.auction_detail, name='auction_detail'),
    path('<int:id>/teklif/', views.bid_view, name='bid_view'),
    path('<int:id>/sonlandir/', views.auction_close, name='auction_close'),
]

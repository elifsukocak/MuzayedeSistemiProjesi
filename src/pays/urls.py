from django.urls import path

from . import views

app_name = 'pays'

urlpatterns = [
    path('', views.odeme_paneli, name='odeme_paneli'),
]

from django import forms
from .models import Urun

class UrunEkleForm(forms.ModelForm):
    class Meta:
        model = Urun
        fields = ['ad', 'aciklama', 'kategori', 'baslangicFiyati', 'gorsel']
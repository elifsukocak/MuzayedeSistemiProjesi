from django import forms
from .models import Urun

class UrunEkleForm(forms.ModelForm):
    class Meta:
        model = Urun
        fields = ['ad', 'aciklama', 'kategori', 'baslangicFiyati', 'gorsel']


class UrunGuncelleForm(forms.ModelForm):
    class Meta:
        model = Urun
        fields = ['ad', 'aciklama', 'kategori', 'baslangicFiyati', 'gorsel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.durum == 'aktif':
            # Tum alanlari kilitlemek icin
            for field_name in self.fields:
                self.fields[field_name].disabled = True

            self.fields['baslangicFiyati'].help_text = "Müzayede aktif olduğu için bilgiler değiştirilemez."
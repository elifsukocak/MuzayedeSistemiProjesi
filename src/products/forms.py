from django import forms
from .models import Urun

class UrunEkleForm(forms.ModelForm):
    class Meta:
        model = Urun
        fields = ['ad', 'aciklama', 'kategori', 'baslangicFiyati', 'artis_adimi', 'teklif_suresi_gun', 'gorsel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['kategori'].empty_label = "Kategori secin"
        self.fields['baslangicFiyati'].widget.attrs.update({'type': 'number', 'min': '0.01', 'step': '0.01'})
        self.fields['artis_adimi'].widget.attrs.update({'type': 'number', 'min': '0.01', 'step': '0.50'})
        self.fields['teklif_suresi_gun'].widget.attrs.update({'type': 'number', 'min': '1', 'step': '1'})


class UrunGuncelleForm(forms.ModelForm):
    class Meta:
        model = Urun
        fields = ['ad', 'aciklama', 'kategori', 'baslangicFiyati', 'artis_adimi', 'teklif_suresi_gun', 'gorsel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['kategori'].empty_label = "Kategori secin"
        self.fields['baslangicFiyati'].widget.attrs.update({'type': 'number', 'min': '0.01', 'step': '0.01'})
        self.fields['artis_adimi'].widget.attrs.update({'type': 'number', 'min': '0.01', 'step': '0.50'})
        self.fields['teklif_suresi_gun'].widget.attrs.update({'type': 'number', 'min': '1', 'step': '1'})

        if self.instance and self.instance.durum == 'aktif':
            # Tum alanlari kilitlemek icin
            for field_name in self.fields:
                self.fields[field_name].disabled = True

            self.fields['baslangicFiyati'].help_text = "Müzayede aktif olduğu için bilgiler değiştirilemez."

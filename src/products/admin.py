from django.contrib import admin
from .models import Kategori, Urun
from django.utils.safestring import mark_safe

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('ad', 'ust_kategori')
    search_fields = ('ad',)
    list_filter = ('ust_kategori',)

@admin.register(Urun)
class UrunAdmin(admin.ModelAdmin):
    list_display = ('ad', 'kategori', 'satici', 'get_durum_renk', 'baslangicFiyati')
    list_filter = ('durum', 'kategori')
    search_fields = ('ad', 'aciklama')

    readonly_fields = ('dinamik_js',)

    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('satici', 'ad', 'aciklama', 'kategori', 'gorsel')
        }),
        ('Müzayede Detayları', {
            'fields': ('baslangicFiyati', 'durum', 'red_sebebi', 'dinamik_js')
        }),
    )

    def dinamik_js(self, obj):
        return mark_safe("""
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    var durumDropdown = document.querySelector('select[name="durum"]');
                    var sebepTextarea = document.querySelector('textarea[name="red_sebebi"]');

                    if (durumDropdown && sebepTextarea) {
                        function durumaGoreKitle() {
                            if (durumDropdown.value === 'reddedildi') {
                                sebepTextarea.removeAttribute('readonly');
                                sebepTextarea.style.backgroundColor = 'white';
                                sebepTextarea.style.pointerEvents = 'auto'; 
                                sebepTextarea.onkeydown = null; 
                            } else {
                                // DİĞER DURUMLAR: Tamamen kilitle
                                sebepTextarea.setAttribute('readonly', 'readonly');
                                sebepTextarea.value = ''; 
                                sebepTextarea.style.backgroundColor = '#eeeeee'; 
                                sebepTextarea.style.pointerEvents = 'none'; 
                                sebepTextarea.onkeydown = function() { return false; }; 
                            }
                        }

                        durumaGoreKitle(); 
                        durumDropdown.addEventListener('change', durumaGoreKitle); 
                    }
                });
            </script>
            <span style="color: green; font-weight: bold;">🔒 Gelişmiş Kilit Sistemi Devrede</span>
        """)

    dinamik_js.short_description = "Sistem Kontrolü"
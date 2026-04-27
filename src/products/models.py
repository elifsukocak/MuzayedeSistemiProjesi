from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Üst Kategori"
    )

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Taslak'),
        ('pending', 'Onay Bekliyor'),
        ('active', 'Aktif'),
        ('sold', 'Satıldı'),
        ('rejected', 'Reddedildi'),
        ('expired', 'Süresi Doldu'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    def __str__(self):
        return self.name

    # DOĞRU YER BURASI (Product Class'ının içi)
    def get_status_display_color(self):
        from django.utils.html import format_html
        colors = {
            'draft': 'gray',
            'pending': 'orange',
            'active': 'green',
            'sold': 'blue',
            'expired': 'red',
            'rejected': 'black',
        }
        color = colors.get(self.status, 'gray')
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            self.get_status_display()
        )
    get_status_display_color.short_description = "Durum"
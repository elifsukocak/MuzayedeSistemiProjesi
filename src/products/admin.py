from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 'status' yerine renkli fonksiyonu buraya ekledik:
    list_display = ('name', 'category', 'seller', 'get_status_display_color', 'starting_price', 'current_price', 'end_time')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')
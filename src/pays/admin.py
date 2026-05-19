from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin): 
	list_display = ('user', 'bakiye', 'guncellenme_tarihi')
	search_fields = ('user__username',)
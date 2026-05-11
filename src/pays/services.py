from decimal import Decimal

from django.db import transaction

from .models import Wallet


def get_wallet(user):
    wallet, _ = Wallet.objects.get_or_create(user=user)
    return wallet


    @transaction.atomic
def add_demo_money(user, amount):
    wallet = Wallet.objects.select_for_update().get_or_create(user=user)[0]
    wallet.bakiye += Decimal(str(amount))
    wallet.full_clean()
    wallet.save(update_fields=['bakiye', 'guncellenme_tarihi'])
    return wallet


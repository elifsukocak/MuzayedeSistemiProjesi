from decimal import Decimal

from django.db import transaction

from .models import Wallet


def get_wallet(user):
    wallet, _ = Wallet.objects.get_or_create(user=user)
    return wallet


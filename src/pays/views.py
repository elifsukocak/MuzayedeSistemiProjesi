from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .services import add_demo_money, get_wallet


@login_required
def odeme_paneli(request):
    wallet = get_wallet(request.user)

    
    if request.method == 'POST':
        try:
            miktar = Decimal(str(request.POST.get('miktar')))
        except (InvalidOperation, TypeError):
            messages.error(request, 'Gecerli bir miktar giriniz.')
            return redirect('pays:odeme_paneli')

        if miktar <= 0:
            messages.error(request, 'Yuklenecek miktar 0 TL uzerinde olmalidir.')
            return redirect('pays:odeme_paneli')       
 
        wallet = add_demo_money(request.user, miktar)
        messages.success(request, f'{miktar} TL demo bakiye eklendi.')
        return redirect('pays:odeme_paneli')

    return render(request, 'pays/odeme.html', {'wallet': wallet})
       

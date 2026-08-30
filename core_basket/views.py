from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core_basket.models import *
from core_menu.models import Instrument
from core_basket.forms import *


@login_required
def basket_items_list(request, basket_id):

    basket = get_object_or_404(Basket, pk=basket_id)

    basket_items_list = BasketItem.objects.filter(basket=basket)

    total_sum = sum(item.product.price * item.quantity
                    for item in basket_items_list)

    return render(request, 
                  'basket/basket_items_list.html', 
                  {'basket_items_list': basket_items_list,
                    'basket': basket,
                    'total_sum': total_sum}
                    )

@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Instrument, pk=product_id)

    basket, created = Basket.objects.get_or_create(account=request.user.account)

    item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('basket-items-list', basket_id=basket.id)

@login_required
def edit_item_quantity(request, basket_id, item_id):
    basket = get_object_or_404(Basket, pk=basket_id)
    item = get_object_or_404(BasketItem, pk=item_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease':
            item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

        return redirect('basket-items-list', basket_id=basket.id)


    return render(request, 
                  'basket/basket_items_list.html', 
                  {'basket': basket, 
                    'item': item})

@login_required
def delete_item(request, basket_id, item_id):
    basket = get_object_or_404(Basket, pk=basket_id)
    item = get_object_or_404(BasketItem, pk=item_id)

    if request.method == 'POST':
        item.delete()

        return redirect('basket-items-list', basket_id=basket.id)


    return render(request, 
                  'basket/delete_item.html', 
                  {'basket': basket,
                    'item': item}
                    )

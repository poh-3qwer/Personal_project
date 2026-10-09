from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from core_order.models import *
from core_basket.models import *
from core_order.forms import*


@login_required
def orders_list(request):
    account = request.user.account
    orders_list = Order.objects.filter(account=account)

    return render(request, 'order/orders_list.html', {'account': account, 'orders_list': orders_list})

@login_required
@transaction.atomic
def create_order(request):
    account = request.user.account
    basket_items = BasketItem.objects.filter(basket__account=account).select_related('product')

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.account = request.user.account
            order.total_price = 0
            order.save()

            total_price = 0
    
            for basket_item in basket_items:

                if basket_item.quantity > basket_item.product.quantity:

                    return render(request, 
                                  'order/create_ordeer.html', 
                                  {'form': form,
                                   'basket_items': basket_items,
                                   'account': account,
                                   'error': f'Недостатньо товару: "{basket_item.product.name}".'}
                                   )

                price = basket_item.product.price
    
                OrderItem.objects.create(
                    order=order,
                    instrument=basket_item.product,
                    quantity=basket_item.quantity,
                    price=price,
                )
    
                total_price += price * basket_item.quantity
                basket_item.product.quantity -= basket_item.quantity
                basket_item.product.save()
    
            order.total_price = total_price
            order.save(update_fields=['total_price'])

            return redirect('order-detail', order_id=order.id)

    else:
        form = OrderForm()
        

    return render(request, 
                  'order/create_order.html', 
                  {'form': form, 
                    'basket_items': basket_items,
                    'account': account,
                    })

@login_required
def order_detail(request, order_id):
    account = request.user.account
    order = get_object_or_404(Order, account=account, pk=order_id)


    return render(request, 
                  'order/order_detail.html', 
                  {'account': account, 
                   'order': order}
                   )

@login_required
@transaction.atomic
def delete_order(request, order_id):
    account = request.user.account
    basket = get_object_or_404(Basket, account=account)
    order = get_object_or_404(Order, account=account, pk=order_id)

    if request.method == 'POST':

        for order_item in order.items.select_related('instrument'):

            instrument = order_item.instrument

            instrument.quantity += order_item.quantity

            instrument.save(update_fields=['quantity'])

        order.delete()

        return redirect('basket-items-list', basket_id=basket.id)


    return render(request, 
                  'order/delete_order.html', 
                  {'account': account,
                    'order': order,
                    'basket': basket}
                    )

@login_required
def payment(request, order_id):
    account = request.user.account
    order = get_object_or_404(Order, pk=order_id, account=request.user.account)

    if request.method == 'POST':
        order.status = 'processing'
        order.save(update_fields=['status'])

        BasketItem.objects.filter(basket__account=account).delete()


        return redirect('order-detail', order_id=order.id)


    return render(request, 
                  'order/payment.html', 
                  {'order': order, 
                   'account': account}
                   )

@login_required
def cancel_order(request, order_id):
    account = request.user.account
    order = get_object_or_404(Order, pk=order_id, account=account)

    if request.method == "POST":
        order.status = 'cancelled'
        order.save(update_fields=['status'])

        return redirect('order-detail', order_id=order.id)

    return render(request, 
                  'order/cancel_order.html',
                   {'order': order,
                    'account': account} 
                    )

@login_required
@transaction.atomic
def sell_message(request, order_id):
    account = request.user.account
    order = get_object_or_404(Order.objects.select_for_update(), pk=order_id)

    seller_items = order.items.filter(
        instrument__salesman = account
    )

    if not seller_items:
        return redirect('home')

    if order.status == 'cancelled':
        return redirect('home')

    if request.method == 'POST':
        seller_items.update(is_shipped=True)

        if not order.items.filter(is_shipped=False).exists():
            order.status = 'shipped'
            order.save(update_fields=['status'])

        return redirect('home')

    return render(request, 
                  'order/sell_message.html', 
                  {'account': account,
                   'order': order}
                   )
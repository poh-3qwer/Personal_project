from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core_menu.models import Instrument
from core_menu.forms import *
from django.http import HttpResponseForbidden
from core_basket.models import Basket
from core_order.models import OrderItem
from django.contrib import messages
from django.core.paginator import Paginator

def instruments_list(request):
    instruments_list = Instrument.objects.all()

    basket = None

    paginator = Paginator(instruments_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(account=request.user.account)

    return render(request, 
                  'menu/instruments_list.html', 
                  {'instruments_list': instruments_list, 
                   'basket': basket,
                   'page_obj': page_obj}
                   )

def instrument_detail(request, instrument_id):
    instrument = get_object_or_404(Instrument, pk=instrument_id)

    instrument_in_orders = OrderItem.objects.filter(instrument=instrument).exists()

    return render(request, 'menu/instrument_detail.html', {'instrument': instrument, 'instrument_in_orders': instrument_in_orders})

@login_required
def add_instrument(request):

    if request.method == 'POST':
        form = InstrumentForm(request.POST, request.FILES)

        if form.is_valid():
            instrument = form.save(commit=False)
            instrument.salesman = request.user.account
            instrument.save()

            return redirect("instruments-list")

    else:
        form = InstrumentForm()


    return render(request, 'menu/add_instrument.html', {'form': form})

@login_required
def edit_instrument_detail(request, instrument_id):
    account = request.user.account
    instrument = get_object_or_404(Instrument, pk=instrument_id)

    if account != instrument.salesman:
        return HttpResponseForbidden('Ви не є власником товару!')

    instrument_in_orders = OrderItem.objects.filter(instrument=instrument).exists()

    if instrument_in_orders:
        messages.error(request, "Не можливо змінити опис товару, після його замовленням кимось!")
                       
        return redirect('instrument-detail', instrument_id=instrument.id)

    if request.method == 'POST':
        form = InstrumentForm(request.POST, request.FILES, instance=instrument)

        if form.is_valid():
            form.save()

            return redirect("instrument-detail", instrument_id=instrument.id)

    else:
        form = InstrumentForm(instance=instrument)


    return render(request, 
                  'menu/edit_instrument.html', 
                  {'form': form,
                   'instrument': instrument,
                   'account': account,
                   'instrument_in_orders': instrument_in_orders}
                   )

@login_required
def delete_instrument(request, instrument_id):
    account = request.user.account
    instrument = get_object_or_404(Instrument, pk=instrument_id)

    if not account.role in ['moderator', 'admin'] and account != instrument.salesman:
        return HttpResponseForbidden('Ви не є власником товару!')

    instrument.delete()

    return redirect("instruments-list")

def instruments_filter(request, category):
    instruments_list_filtered = Instrument.objects.filter(category=category)

    paginator = Paginator(instruments_list_filtered, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 
                  'menu/instruments_filter.html', 
                  {'instruments_list_filtered': page_obj, 
                   'category': category,
                   'page_obj': page_obj}
                   )


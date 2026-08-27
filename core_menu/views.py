from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core_menu.models import Instrument
from core_menu.forms import *
from django.http import HttpResponseForbidden


def instruments_list(request):
    instruments_list = Instrument.objects.all()

    return render(request, 'menu/instruments_list.html', {'instruments_list': instruments_list})

def instrument_detail(request, instrument_id):
    instrument = get_object_or_404(Instrument, pk=instrument_id)

    return render(request, 'menu/instrument_detail.html', {'instrument': instrument})

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
                   'account': account}
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

    return render(request, 'menu/instruments_filter.html', {'instruments_list_filtered': instruments_list_filtered, 'category': category})
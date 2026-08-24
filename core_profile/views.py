from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core_profile.models import Account
from core_profile.forms import *


@login_required
def account(request):
    account = get_object_or_404(Account, user=request.user)
    account.auto_give_role()


    return render(request, 'account/account.html', {'account': account})

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)


    return render(request, 'account/account_detail.html', {'account': account})

@login_required
def change_account_detail(request, account_id):
    account = get_object_or_404(Account, user=request.user, pk=account_id)

    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()

            return redirect('account-detail', account_id=account_id)
    else:
        form = AccountForm(instance=account)

    return render(request, 'account/edit_account_detail.html', {'form': form, 'account': account})

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id, user=request.user)

    if request.method == 'POST':
        account.user.delete()

        return redirect('home')


    return render(request, 'account/delete_account.html', {'account': account})



#! Ссылка на домашнюю страницу - не трогать!
def home(request):
    return render(request, 'home.html')
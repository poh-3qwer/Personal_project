from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core_auth_system.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django .contrib .auth import login ,logout 


def register_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            account = user.account
            account.human_name = form.cleaned_data['human_name']
            account.human_surname = form.cleaned_data['human_surname']
            account.save()
            
            login(request, user)

            return redirect('account')
    else:
        form = RegisterUserForm()


    return render(request, 'auth_system/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect('account')
    else:
        form = AuthenticationForm(request)


    return render(request, 'auth_system/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
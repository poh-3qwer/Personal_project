from django.urls import path
from core_profile.views import *


urlpatterns = [
    # --- home ---
    path('home', home, name='home'),
    # ------
    path('account', account, name='account'),
    path('account-detail/<int:account_id>/', account_detail, name='account-detail'),
    path('change-account-detail/<int:account_id>/', change_account_detail, name='change-account-detail'),
    path('delete-account/<int:account_id>/', delete_account, name='delete-account'),
]
from django.urls import path
from core_auth_system.views import *


urlpatterns = [
    path('register', register_view, name='register'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
]
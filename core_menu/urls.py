from django.urls import path
from core_menu.views import *


urlpatterns = [
    path('instruments-list/', instruments_list, name='instruments-list'),
    path('instrument-detail/<int:instrument_id>/', instrument_detail, name='instrument-detail'),
    path('add-instrument/', add_instrument, name='add-instrument'),
    path('edit-instrument-detail/<int:instrument_id>/', edit_instrument_detail, name='edit-instrument-detail'),
    path('delete-instrument/<int:instrument_id>/', delete_instrument, name='delete-instrument'),
    path('instruments-filter/<str:category>/', instruments_filter, name='instruments-filter'),
]
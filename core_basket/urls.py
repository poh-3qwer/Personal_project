from django.urls import path
from core_basket.views import *


urlpatterns = [
    path('basket-items-list/<int:basket_id>/', basket_items_list, name='basket-items-list'),
    path('add-to-basket/<int:product_id>/', add_to_basket, name='add-to-basket'),
    path('edit-item-quantity/<int:basket_id>/<int:item_id>/', edit_item_quantity, name='edit-item-quantity'),
    path('delete-item/<int:basket_id>/<int:item_id>/', delete_item, name='delete-item'),
]
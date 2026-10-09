from django.urls import path
from core_order.views import *


urlpatterns = [
    path('orders-list/', orders_list, name='orders-list'),
    path('create-order/', create_order, name='create-order'),
    path('order-detail/<int:order_id>/', order_detail, name='order-detail'),
    path('delete-order/<int:order_id>/', delete_order, name='delete-order'),
    path('payment/<int:order_id>/', payment, name='payment'),
    path('cancel-order/<int:order_id>/', cancel_order, name='cancel-order'),
    path('sell-message/<int:order_id>/', sell_message, name='sell-message'),
]
from core_order.models import Order, OrderItem
from core_menu.models import Instrument


def orders_list(request):
    if request.user.is_authenticated:
        return {
            'orders_list': Order.objects.filter(account=request.user.account)
        }

    return {
        'orders_list': []
    }

def has_products(request):
    if request.user.is_authenticated:
        has_products = Instrument.objects.filter(
            salesman=request.user.account
        ).exists()
    else:
        has_products=False

    return {'has_products_for_sale': has_products}

def has_products_to_ship(request):

    if not request.user.is_authenticated:
        return {
            'has_products_to_ship': False,
            'products_to_ship': [],
        }

    products_to_ship = OrderItem.objects.filter(instrument__salesman=request.user.account, is_shipped=False).select_related('order', 'instrument')

    return {'has_products_to_ship': products_to_ship.exists, 'products_to_ship': products_to_ship}

def has_cancelled_order(request):
    if not request.user.is_authenticated:
        return {'has_cancelled_order': False,
                'cancelled_orders': []
                }

    account = request.user.account

    cancelled_orders = Order.objects.filter(status='cancelled', items__instrument__salesman = account).distinct()

    has_cancelled_order = cancelled_orders.exists()

    return {'has_cancelled_order': has_cancelled_order, 'cancelled_orders': cancelled_orders}
from projects.apps.order.models import Order

def create_order():
    order = Order()
    order.save()
    return order
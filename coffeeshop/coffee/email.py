from django.conf import settings
from django.core.mail import send_mail


def send_mail_order_updated(product_order):
    message = (
        f"Hello {product_order.user.username}, \n\n"
        f"The status of your Product {product_order.product.name} is updated to {product_order.status}. \n\n"
        f"Thank You."
    )
    send_mail(
        "Product Status Updated",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[product_order.user.email],
        fail_silently=True,
    )

from django.contrib.auth.models import User
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail

def order_notification_to_user():
    pass


def find_nearest_pharmacy():
    return {"pharmacy":1}

def check_drug_availability(pharmacy):
    return True

def order_notification_to_pharmacy(pharmacy):
    print("order notification sent to pharmacy")

def process_order():
    pharmacy = find_nearest_pharmacy()
    if check_drug_availability(pharmacy):
        order_notification_to_pharmacy(pharmacy)

def notify_user(instance):
    body = 'Dear Customer, Your order status updated now, Current status of the is {}.'.format(instance.status)
    subject = "Order Status Update"
    user_email = User.objects.filter(id =instance.user_id).first().email
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)

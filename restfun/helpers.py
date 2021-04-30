from django.core.mail import send_mail

def send_email(mail_to,subject='Contact from RESTFun', message='Message from our team', mail_from='restfun@restfun.com.br'):
    send_mail(
        subject,
        message,
        mail_from,
        mail_to,
        fail_silently=False,
    )
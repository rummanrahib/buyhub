from celery import shared_task
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import Account


# Send Mail to All Users
@shared_task(bind=True)
def send_mail_func(self):
    users = Account.objects.all()
    for user in users:

        if user.is_active and not user.is_admin:

            mail_subject = 'Celery Email Testing!'
            message = "Hello there, hope you're doing great! Thanks for being with BuyHub. Check out our new collection of products and services. We hope you enjoy your shopping experience with us. Happy Shopping!"
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send(fail_silently=True)

    return 'Done Sending Mail to All Users...'
# ...


# Send Confirmation Mail to User
@shared_task(bind=True)
def send_confirmation_mail_func(self, user_id):
    user = Account.objects.get(id=user_id)
    email = user.email
    current_site = '127.0.0.1:8000'
    mail_subject = 'Please activate your BuyHub account'
    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    return 'Done Sending Confirmation Mail to User...'
# ...

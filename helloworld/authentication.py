from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.http import HttpResponse, HttpRequest

def activate_email(request: HttpRequest, user, to_email):
    """
    Builds and sends an email for user verification

    Parameters:
    request (HttpRequest): incoming HTTP request
    user: User object
    to_email: recipient email address

    Returns:
    None
    """
    mail_subject = "Activate User Account"
    message = render_to_string(
        "activate_user.html", {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http'
        }
    )

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
        html_message=message
    )

    messages.success(request, f'Dear {user.username}, please go to {to_email} inbox/spam & click on received activation link to confirm and complete the registration.')
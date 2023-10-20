import logging

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()


logger = logging.getLogger(__name__)


@shared_task
def send_new_user_email(user_id: int) -> None:
    user = User.objects.get(id=user_id)

    if not user:
        logger.error(
            f"Trying to send new user email for non-existent user id { user_id }"
        )
        return

    context = {
        "title": "Welcome",
        "first_name": user.first_name,
        "password": settings.NEW_USER_PASSWORD,
        "site_address": settings.SITE_ADDRESS,
    }

    html_message = render_to_string("email/new_user.html", context)
    plain_message = render_to_string("email/new_user.txt", context)

    send_mail(
        subject="Welcome",
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        message=plain_message,
        html_message=html_message,
    )

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache


@shared_task
def send_verification_email(email, token, expires_in=300):
    # Save token in cache with expiration
    cache.set(f"verification_token_{token}", email, expires_in)

    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    send_mail(
        "Verify your email",
        f"Please verify your email by clicking this link: {verification_url}\n"
        f"This link will expire in 5 minutes.",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

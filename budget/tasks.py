from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

@shared_task(bind=True, max_retries=3)
def send_email_async(self, subject, message, recipients, from_email=None):
    try:
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL
        if isinstance(recipients, str):
            recipients = [recipients]
        # simple text email
        EmailMultiAlternatives(subject, message, from_email, recipients).send(fail_silently=False)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)

@shared_task(bind=True, max_retries=3)
def send_html_email_async(self, subject, text_body, html_body, recipients, from_email=None):
    try:
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL
        if isinstance(recipients, str):
            recipients = [recipients]
        msg = EmailMultiAlternatives(subject, text_body, from_email, recipients)
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

User = get_user_model()






# @shared_task
# def send_registration_email(user_id, raw_password):
#     try:
#         user = User.objects.get(id=user_id)
#         subject = "Welcome to Our Platform!"
#         message = (
#             f"Hello {user.first_name},\n\n"
#             f"Your login credentials:\n\n"
#             f"Username: {user.username}\n"
#             f"Email: {user.email}\n"
#             f"Password: {raw_password}\n\n"
#             "Best regards,\nYour Support Team"
#         )

#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False,
#         )

#         logger.info(f"Email sent successfully to {user.email}")

#     except User.DoesNotExist:
#         logger.error(f"User with ID {user_id} not found.")
#     except Exception as e:
#         logger.error(f"Error sending registration email: {str(e)}")






# Celery Task for Sending Emails
# @shared_task
# def send_registration_email(user_id, raw_password):
#     """Send registration email asynchronously."""
#     try:
#         user = User.objects.get(id=user_id)
#         subject = "Welcome to Our Platform!"
#         message = (
#             f"Hello {user.first_name},\n\n"
#             f"Your login credentials:\n\n"
#             f"Username: {user.username}\n"
#             f"Email: {user.email}\n"
#             f"Password: {raw_password}\n\n"
#             "Best regards,\nYour Support Team"
#         )

#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False,
#         )

#         logger.info(f"Email sent successfully to {user.email}")

#     except User.DoesNotExist:
#         logger.error(f"User with ID {user_id} not found.")
#     except Exception as e:
#         logger.error(f"Error sending registration email: {str(e)}")


def send_registration_email_sync(user_id, raw_password):
    """Send registration email synchronously (fallback if Celery fails)."""
    try:
        user = User.objects.get(id=user_id)
        subject = "Welcome to Project Tracker!"
        message = (
            f"Hello {user.username},\n\n"
            f"Your account has been created.\nEmail: {user.email}\n"
            f"Password: {raw_password}\n\n"
            "Please log in and change your password."
        )

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        logger.info(f"Synchronous email sent successfully to {user.email}")

    except Exception as e:
        logger.error(f"Sync fallback email failed: {e}")


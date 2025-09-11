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


from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from decimal import Decimal
from .models import Project, ProjectPaymentTracking, ProjectEstimation

@shared_task
def recalculate_project_finances(project_id):
    """
    Background task to recalculate project financials
    and update profit/loss without blocking the API request.
    """
    try:
        project = Project.objects.get(id=project_id)
        estimation = ProjectEstimation.objects.filter(project=project).last()
        payments = ProjectPaymentTracking.objects.filter(project=project)

        approved_budget = estimation.approved_amount if estimation else Decimal("0.00")
        actuals = sum(p.approved_budget for p in payments)
        payout = sum(p.payout for p in payments)
        pending = approved_budget - payout

        profit_loss = payout - actuals

        # Save computed values (can store in Project or FinancialSnapshot model)
        project.last_recalculated_at = now()
        project.profit_loss = profit_loss
        project.pending_amount = pending
        project.save(update_fields=["last_recalculated_at", "profit_loss", "pending_amount"])

        return f"Project {project.id} recalculated successfully."

    except Project.DoesNotExist:
        return f"Project {project_id} does not exist."


@shared_task
def send_budget_alerts(project_id):
    """
    Alert when project cost exceeds estimation or approaches the limit.
    """
    try:
        project = Project.objects.get(id=project_id)
        estimation = ProjectEstimation.objects.filter(project=project).last()
        payments = ProjectPaymentTracking.objects.filter(project=project)

        if not estimation:
            return f"No estimation found for project {project_id}"

        approved_budget = estimation.approved_amount or Decimal("0.00")
        actuals = sum(p.approved_budget for p in payments)

        # Check threshold (90% of estimation reached)
        if actuals >= approved_budget * Decimal("0.9") and actuals < approved_budget:
            message = f"⚠️ Warning: Project {project.name} has reached 90% of approved budget."
        elif actuals >= approved_budget:
            message = f"🚨 Alert: Project {project.name} has EXCEEDED the approved budget!"
        else:
            return f"Project {project_id} is within budget."

        # Example: send an email (you can replace with Slack/Teams/etc.)
        send_mail(
            subject=f"Budget Alert for Project {project.name}",
            message=message,
            from_email="noreply@yourapp.com",
            recipient_list=["finance-team@yourcompany.com"],
            fail_silently=True,
        )

        return message

    except Project.DoesNotExist:
        return f"Project {project_id} does not exist."

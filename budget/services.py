from django.utils import timezone
from .tasks import send_email_async, send_html_email_async
from django.template.loader import render_to_string

def _listify(recipients):
    # allow single string or list
    if not recipients:
        return []
    return recipients if isinstance(recipients, (list, tuple)) else [recipients]

# def notify_budget_request(obj, recipients):
#     subject = f"[Action Required] Budget Request for {obj.payment_tracking.project.project_name}"
#     context = {
#         "project": obj.payment_tracking.project.project_name,
#         "amount": obj.requested_amount,
#         "reason": obj.reason,
#         "requested_by": str(obj.created_by),
#         "date": timezone.localtime(obj.created_at).strftime("%Y-%m-%d %H:%M"),
#         "request_id": obj.id,
#     }
#     body = render_to_string("finance/emails/budget_request.txt", context)
#     html = render_to_string("finance/emails/budget_request.html", context)
#     send_html_email_async.delay(subject, body, html, _listify(recipients))

# def notify_budget_approved(obj, recipients):
#     subject = f"[Approved] Budget Request for {obj.payment_tracking.project.project_name}"
#     context = {"project": obj.payment_tracking.project.project_name, "amount": obj.requested_amount, "approved_by": str(obj.approved_by), "approved_at": timezone.localtime(obj.approved_at).strftime("%Y-%m-%d %H:%M")}
#     body = render_to_string("finance/emails/budget_approved.txt", context)
#     html = render_to_string("finance/emails/budget_approved.html", context)
#     send_html_email_async.delay(subject, body, html, _listify(recipients))

# def notify_budget_rejected(obj, recipients):
#     subject = f"[Rejected] Budget Request for {obj.payment_tracking.project.project_name}"
#     context = {"project": obj.payment_tracking.project.project_name, "amount": obj.requested_amount, "approved_by": str(obj.approved_by), "notes": obj.approval_notes}
#     body = render_to_string("finance/emails/budget_rejected.txt", context)
#     html = render_to_string("finance/emails/budget_rejected.html", context)
#     send_html_email_async.delay(subject, body, html, _listify(recipients))
from django.utils import timezone
from .tasks import send_email_async

def notify_budget_request(request_obj):
    """Notify finance head for approval request"""
    subject = f"Approval Required: Additional Budget for {request_obj.payment_tracking.project.project_name}"
    message = f"""
A request for an additional budget has been raised.

Project: {request_obj.payment_tracking.project.project_name}
Requested Amount: {request_obj.requested_amount}
Reason: {request_obj.reason or 'N/A'}
Requested By: {request_obj.created_by}
Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}
    """

    recipients = ["finance-head@company.com"]  # fetch dynamically in real apps
    send_email_async.delay(subject, message, recipients)


def notify_budget_approval(request_obj):
    subject = f"Budget Request Approved - {request_obj.payment_tracking.project.project_name}"
    message = f"""
Your budget request has been approved.

Project: {request_obj.payment_tracking.project.project_name}
Approved Amount: {request_obj.requested_amount}
Approved By: {request_obj.approved_by}
Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}
    """
    recipients = [request_obj.created_by.email]
    send_email_async.delay(subject, message, recipients)


def notify_budget_rejection(request_obj):
    subject = f"Budget Request Rejected - {request_obj.payment_tracking.project.project_name}"
    message = f"""
Your budget request has been rejected.

Project: {request_obj.payment_tracking.project.project_name}
Requested Amount: {request_obj.requested_amount}
Reviewed By: {request_obj.approved_by}
Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}
    """
    recipients = [request_obj.created_by.email]
    send_email_async.delay(subject, message, recipients)


# def notify_milestone_update(milestone_obj):
#     subject = f"Milestone Update - {milestone_obj.payment_tracking.project.project_name}"
#     message = f"""
# Milestone '{milestone_obj.name}' has been updated.

# Status: {milestone_obj.status}
# Amount: {milestone_obj.amount}
# Due Date: {milestone_obj.due_date}
# Notes: {milestone_obj.notes or 'N/A'}
#     """
#     recipients = ["project-owner@company.com", "finance@company.com"]
#     send_email_async.delay(subject, message, recipients)


def notify_budget_breach(payment_obj):
    subject = f"⚠️ Budget Breach Alert - {payment_obj.project.project_name}"
    message = f"""
Warning: The budget has been exceeded!

Project: {payment_obj.project.project_name}
Approved + Additional Budget: {payment_obj.total_available_budget}
Total Milestones: {payment_obj.total_milestones_amount}
Payout: {payment_obj.payout}
Pending: {payment_obj.pending}
    """
    recipients = ["cfo@company.com", "finance@company.com"]
    send_email_async.delay(subject, message, recipients)


# def notify_milestone_update(milestone, recipients):
#     subject = f"Milestone Update: {milestone.payment_tracking.project.project_name} - {milestone.name}"
#     context = {"milestone": milestone}
#     body = render_to_string("finance/emails/milestone_update.txt", context)
#     html = render_to_string("finance/emails/milestone_update.html", context)
#     send_html_email_async.delay(subject, body, html, _listify(recipients))

def notify_budget_breach(payment, recipients):
    subject = f"Budget Exceeded: {payment.project.project_name}"
    context = {"payment": payment}
    body = render_to_string("finance/emails/budget_breach.txt", context)
    html = render_to_string("finance/emails/budget_breach.html", context)
    send_html_email_async.delay(subject, body, html, _listify(recipients))



from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import ProjectPaymentTracking, ProjectPaymentMilestone, PaymentTransaction, AdditionalBudgetRequest, PaymentHistory
from django.db.models import Sum
from .exceptions import ObjectNotFound

def get_payment(payment_id):
    try:
        return ProjectPaymentTracking.objects.get(pk=payment_id)
    except ProjectPaymentTracking.DoesNotExist:
        raise ObjectNotFound(f"Payment tracking {payment_id} not found")

def create_payment(validated_data, user):
    validated_data["created_by"] = user
    validated_data["modified_by"] = user
    return ProjectPaymentTracking.objects.create(**validated_data)

def update_payment(payment_id, validated_data, user):
    payment = get_payment(payment_id)
    # Basic check: payout cannot exceed total_available_budget if provided
    if "payout" in validated_data:
        new_payout = validated_data.get("payout")
        total_available = payment.total_available_budget
        if new_payout > total_available:
            raise ValidationError({"payout": f"Payout ({new_payout}) cannot exceed total available budget ({total_available})."})
        # Also check payout <= completed milestones - enforced elsewhere for transactions.
    for k, v in validated_data.items():
        setattr(payment, k, v)
    payment.modified_by = user
    payment.save()
    return payment

def delete_payment(payment_id):
    p = get_payment(payment_id)
    p.delete()
    return True


from decimal import Decimal
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
from .models import ProjectPaymentMilestone, ProjectPaymentTracking
from .exceptions import ObjectNotFound

def create_milestone(validated_data, user, enforce_budget=True):
    payment = validated_data["payment_tracking"]
    amount = validated_data["amount"]
    if amount <= Decimal("0.00"):
        raise ValidationError({"amount": "Milestone amount must be positive."})

    if enforce_budget:
        existing_total = payment.total_milestones_amount
        projected = existing_total + amount
        available = payment.total_available_budget
        if projected > available and not payment.budget_exceeded_approved:
            raise ValidationError({"__all__": f"Total milestones ({projected}) cannot exceed available budget ({available})."})

    m = ProjectPaymentMilestone.objects.create(
        payment_tracking=payment,
        name=validated_data["name"],
        amount=amount,
        due_date=validated_data.get("due_date"),
        status=validated_data.get("status", "Planned"),
        notes=validated_data.get("notes"),
        created_by=user,
        modified_by=user
    )
    return m

# def update_milestone(milestone_id, validated_data, user):
#     try:
#         m = ProjectPaymentMilestone.objects.get(pk=milestone_id)
#     except ProjectPaymentMilestone.DoesNotExist:
#         raise ObjectNotFound(f"Milestone {milestone_id} not found")
#     if "status" in validated_data and validated_data["status"] == "Completed" and not m.actual_completion_date:
#         m.actual_completion_date = m.actual_completion_date or None
#     for k, v in validated_data.items():
#         setattr(m, k, v)
#     m.modified_by = user
#     m.save()
#     return m
# def notify_milestone_update(milestone_obj):
#     subject = f"Milestone Update - {milestone_obj.payment_tracking.project.project_name}"
#     message = f"""
# Milestone '{milestone_obj.name}' has been updated.

# Status: {milestone_obj.status}
# Amount: {milestone_obj.amount}
# Due Date: {milestone_obj.due_date}
# Notes: {milestone_obj.notes or 'N/A'}
#     """
#     recipients = ["project-owner@company.com", "finance@company.com"]
#     send_email_async.delay(subject, message, recipients)
def notify_milestone_update(milestone_obj, extra_emails=None):
    subject = f"Milestone Update - {milestone_obj.payment_tracking.project.project_name}"
    message = f"""
Milestone '{milestone_obj.name}' has been updated.

Status: {milestone_obj.status}
Amount: {milestone_obj.amount}
Due Date: {milestone_obj.due_date}
Notes: {milestone_obj.notes or 'N/A'}
    """
    # default recipients
    recipients = ["project-owner@company.com", "finance@company.com"]
    
    # add extra emails if provided
    if extra_emails:
        recipients.extend(extra_emails)

    # send the email asynchronously
    send_email_async.delay(subject, message, recipients)



def notify_budget_breach(payment_obj):
    subject = f"⚠️ Budget Breach Alert - {payment_obj.project.project_name}"
    message = f"""
Warning: The budget has been exceeded!

Project: {payment_obj.project.project_name}
Approved + Additional Budget: {payment_obj.total_available_budget}
Total Milestones: {payment_obj.total_milestones_amount}
Payout: {payment_obj.payout}
Pending: {payment_obj.pending}
    """
    recipients = ["cfo@company.com", "finance@company.com"]
    send_email_async.delay(subject, message, recipients)

def delete_milestone(milestone_id):
    try:
        m = ProjectPaymentMilestone.objects.get(pk=milestone_id)
    except ProjectPaymentMilestone.DoesNotExist:
        raise ObjectNotFound(f"Milestone {milestone_id} not found")
    m.delete()
    return True



from decimal import Decimal
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import PaymentTransaction, ProjectPaymentTracking
from django.db.models import Sum
from .exceptions import ObjectNotFound

def create_transaction(payment_id, amount, user, method=None, notes=None):
    payment = ProjectPaymentTracking.objects.get(pk=payment_id)
    if amount <= Decimal("0.00"):
        raise ValidationError({"amount": "Transaction must be positive."})

    completed_total = payment.completed_milestones_amount
    # Payout after transaction should not exceed completed milestones nor total_available_budget
    if (payment.payout + amount) > completed_total:
        raise ValidationError({"amount": f"Payout after this transaction ({payment.payout + amount}) cannot exceed completed milestones total ({completed_total})."})

    if (payment.payout + amount) > payment.total_available_budget:
        raise ValidationError({"amount": f"Payout after this transaction ({payment.payout + amount}) cannot exceed total available budget ({payment.total_available_budget})."})

    with transaction.atomic():
        payment = ProjectPaymentTracking.objects.select_for_update().get(pk=payment_id)
        payment.payout = (payment.payout or Decimal("0.00")) + amount
        payment.modified_by = user
        payment.save()

        tx = PaymentTransaction.objects.create(
            payment_tracking=payment, amount=amount, method=method, notes=notes, created_by=user
        )
    return tx


from django.db import transaction
from django.utils import timezone
from .models import AdditionalBudgetRequest, ProjectPaymentTracking
from rest_framework.exceptions import ValidationError
from .exceptions import ObjectNotFound

def request_additional(payment_id, amount, reason, user):
    payment = ProjectPaymentTracking.objects.get(pk=payment_id)
    req = AdditionalBudgetRequest.objects.create(payment_tracking=payment, requested_amount=amount, reason=reason, created_by=user)
    return req

@transaction.atomic
def approve_request(req_id, approver_user, notes=""):
    try:
        req = AdditionalBudgetRequest.objects.select_for_update().get(pk=req_id)
    except AdditionalBudgetRequest.DoesNotExist:
        raise ObjectNotFound(f"AdditionalBudgetRequest {req_id} not found")

    if req.status == AdditionalBudgetRequest.STATUS_APPROVED:
        raise ValidationError("Already approved")

    if req.status == AdditionalBudgetRequest.STATUS_REJECTED:
        raise ValidationError("Already rejected")

    pt = ProjectPaymentTracking.objects.select_for_update().get(pk=req.payment_tracking_id)
    pt.additional_amount = (pt.additional_amount or 0) + (req.requested_amount or 0)
    pt.budget_exceeded_approved = pt.is_budget_exceeded or pt.budget_exceeded_approved
    pt.modified_by = approver_user
    pt.save()

    req.status = AdditionalBudgetRequest.STATUS_APPROVED
    req.approved_by = approver_user
    req.approved_at = timezone.now()
    req.approval_notes = notes
    req.save()
    return req

@transaction.atomic
def reject_request(req_id, approver_user, notes=""):
    try:
        req = AdditionalBudgetRequest.objects.select_for_update().get(pk=req_id)
    except AdditionalBudgetRequest.DoesNotExist:
        raise ObjectNotFound(f"AdditionalBudgetRequest {req_id} not found")

    if req.status != AdditionalBudgetRequest.STATUS_PENDING:
        raise ValidationError("Only pending requests can be rejected")

    req.status = AdditionalBudgetRequest.STATUS_REJECTED
    req.approved_by = approver_user
    req.approved_at = timezone.now()
    req.approval_notes = notes
    req.save()
    return req



from decimal import Decimal
from .models import Rule, Notification

def evaluate_rule(rule, payment):
    val = None
    if rule.type == "budget_utilization":
        val = payment.budget_utilization_percentage
    elif rule.type == "pending_percentage":
        total = payment.total_available_budget
        if total == Decimal("0.00"):
            return False
        val = (payment.pending / total) * Decimal("100.00")
    elif rule.type == "completed_milestones":
        val = payment.completed_milestones_amount
    else:
        return False

    op = rule.operator
    if op == "gt":
        return val > rule.value
    if op == "gte":
        return val >= rule.value
    if op == "lt":
        return val < rule.value
    if op == "lte":
        return val <= rule.value
    return False

def evaluate_and_notify(payment):
    rules = Rule.objects.filter(is_enabled=True)
    for r in rules:
        try:
            if evaluate_rule(r, payment):
                # notify project owner (if exists) as example
                if payment.created_by:
                    Notification.objects.create(
                        recipient=payment.created_by,
                        title=f"Rule triggered: {r}",
                        message=f"Rule {r} triggered for payment {payment.id}",
                        data={"payment_id": payment.id, "rule_id": r.id}
                    )
        except Exception:
            continue

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import ProjectPaymentTracking, AuditLog, PaymentHistory, ProjectPaymentMilestone
from django.forms.models import model_to_dict
from .services import evaluate_and_notify
from django.conf import settings

@receiver(pre_save, sender=ProjectPaymentTracking)
def capture_old(sender, instance, **kwargs):
    try:
        instance._old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        instance._old_instance = None

@receiver(post_save, sender=ProjectPaymentTracking)
def log_changes(sender, instance, created, **kwargs):
    old = getattr(instance, "_old_instance", None)
    if old:
        tracked = ["approved_budget", "additional_amount", "payout", "hold", "retention_amount", "penalty_amount"]
        for f in tracked:
            old_v = getattr(old, f)
            new_v = getattr(instance, f)
            if str(old_v) != str(new_v):
                AuditLog.objects.create(model_name="ProjectPaymentTracking", object_id=str(instance.pk), field_name=f, old_value=str(old_v), new_value=str(new_v), changed_by=instance.modified_by)
                PaymentHistory.objects.create(payment_tracking=instance, field_changed=f, prev_value=str(old_v), new_value=str(new_v), changed_by=instance.modified_by)
    # Post-save evaluate rules
    try:
        evaluate_and_notify(instance)
    except Exception:
        pass

@receiver(post_save, sender=ProjectPaymentMilestone)
def milestone_post_save(sender, instance, created, **kwargs):
    # If completed, trigger rule evaluation for its payment tracking
    try:
        evaluate_and_notify(instance.payment_tracking)
    except Exception:
        pass

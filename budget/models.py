from django.db import models
# Create your models here.
from project_creation.models import Project
from login.models import User,BaseModel
from roles.models import UserRole
from django.utils import timezone
from project_creation.models import Client
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
import os
from django.db.models import Sum
from masterdata.models import MasterData
from decimal import Decimal
from django.db import models, transaction
from django.utils import timezone
from masterdata.models import MasterData
from django.db.models.functions import Coalesce

from django.db.models import Sum, Value, DecimalField
 
# Create your models here.


class ProjectEstimation(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name="estimations", null=True, blank=True)
    estimation_date = models.DateField()
    estimation_provider = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="estimations_provided", null=True, blank=True)
    estimation_review = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="estimations_reviewed", null=True, blank=True)
    estimation_review_by_client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_estimations")
    
    version = models.PositiveIntegerField(default=1)
    initial_estimation_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    PURCHASE_ORDER_STATUS = [
        ('Received', 'Received'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]
    purchase_order_status = models.CharField(max_length=50, choices=PURCHASE_ORDER_STATUS, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="estimations_created")
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="estimations_modified")

    class Meta:
        # unique_together = ("project", "version")
        ordering = ["-created_at"]

    def __str__(self):
        status = " (Approved)" if self.is_approved else ""
        return f"{self.project.project_name} - v{self.version}{status}"\
    @classmethod
    def latest_estimation(cls, project):
        """Get the latest approved estimation for a project"""
        return cls.objects.filter(project=project, is_approved=True).order_by("-version").first()




# class ChangeRequest(models.Model):
#     STATUS_PENDING = "Pending"
#     STATUS_APPROVED = "Approved"
#     STATUS_REJECTED = "Rejected"

#     STATUS_CHOICES = [
#         (STATUS_PENDING, "Pending"),
#         (STATUS_APPROVED, "Approved"),
#         (STATUS_REJECTED, "Rejected"),
#     ]

#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="change_requests")
#     requested_amount = models.DecimalField(max_digits=18, decimal_places=2)
#     reason = models.TextField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

#     requested_by = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="cr_requested"
#     )
#     reviewed_by = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, blank=True, related_name="cr_reviewed"
#     )
#     reviewed_at = models.DateTimeField(null=True, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)

#     # optional correlation id for dedupe/intent
#     correlation_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)

#     class Meta:
#         ordering = ["-created_at"]

#     def _str_(self):
#         return f"CR #{self.id} for {getattr(self.project, 'project_name', self.project_id)} - {self.requested_amount}"

#     def approve(self, reviewer_user):
#         from .services import BudgetMonitorService

#         if self.status != self.STATUS_PENDING:
#             raise ValueError("Only pending CRs can be approved")

#         with transaction.atomic():
#             self.status = self.STATUS_APPROVED
#             self.reviewed_by = reviewer_user
#             self.reviewed_at = timezone.now()
#             self.save(update_fields=["status", "reviewed_by", "reviewed_at", "modified_at"])

#             # create new estimation row (versioned) to preserve history
#             latest = ProjectEstimation.objects.filter(project=self.project).order_by("-version", "-created_at").first()

#             if latest:
#                 version = (latest.version or 1) + 1
#                 base_initial = latest.initial_estimation_amount or Decimal("0.00")
#                 base_approved = latest.approved_amount if latest.approved_amount is not None else base_initial
#             else:
#                 version = 1
#                 base_initial = Decimal("0.00")
#                 base_approved = Decimal("0.00")

#             new_approved_amount = (base_approved or Decimal("0.00")) + (self.requested_amount or Decimal("0.00"))

#             ProjectEstimation.objects.create(
#                 project=self.project,
#                 estimation_date=timezone.now().date(),
#                 estimation_provider=None,
#                 estimation_review=None,
#                 version=version,
#                 initial_estimation_amount=base_initial,
#                 approved_amount=new_approved_amount,
#                 is_approved=True,
#                 purchase_order_status="Received",
#                 created_by=reviewer_user,
#                 modified_by=reviewer_user,
#             )

#             # audit
#             AuditLog.log(
#                 self.project,
#                 reviewer_user,
#                 "change_request.approved",
#                 {
#                     "cr_id": self.id,
#                     "requested_amount": str(self.requested_amount),
#                     "new_approved_amount": str(new_approved_amount),
#                 },
#             )

#             # trigger immediate monitoring after approval
#             BudgetMonitorService.monitor_project(self.project)

#     def reject(self, reviewer_user):
#         if self.status != self.STATUS_PENDING:
#             raise ValueError("Only pending CRs can be rejected")

#         self.status = self.STATUS_REJECTED
#         self.reviewed_by = reviewer_user
#         self.reviewed_at = timezone.now()
#         self.save(update_fields=["status", "reviewed_by", "reviewed_at", "modified_at"])

#         AuditLog.log(
#             self.project, reviewer_user, "change_request.rejected", {"cr_id": self.id}
#         )


# Prefer importing Project from your project_creation app.
# If you DO NOT have a separate Project model, uncomment the local Project class below.
try:
    from project_creation.models import Project
except Exception:
  
    raise


CURRENCY_CHOICES = [
    ("INR", "Indian Rupee"),
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
]
class ProjectPaymentTracking(models.Model):
    COST_TYPE_CHOICES = [
        ("Manpower", "Manpower"),
        ("Operation Cost", "Operation Cost"),
        ("Transport", "Transport"),
        ("Interest", "Interest"),
        ("Other", "Other"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="payments")
    payment_type = models.CharField(max_length=50, choices=COST_TYPE_CHOICES)
    resource = models.ForeignKey(MasterData, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")
    currency = models.CharField(max_length=6, choices=CURRENCY_CHOICES, default="INR")

    approved_budget = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))
    additional_amount = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))

    payout = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))
    retention_amount = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))
    penalty_amount = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))

    is_budget_locked = models.BooleanField(default=False)
    budget_exceeded_approved = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payment_created")
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payment_modified")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project Payment Tracking"
        verbose_name_plural = "Project Payment Trackings"

    def __str__(self):
        return f"{getattr(self.project, 'project_name', self.project_id)} - {self.payment_type} (#{self.id})"

    # @property
    # def total_available_budget(self) -> Decimal:
    #     return (self.approved_budget or Decimal("0.00")) + (self.additional_amount or Decimal("0.00"))

    # @property
    # def total_milestones_amount(self) -> Decimal:
    #     return self.milestones.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    # @property
    # def completed_milestones_amount(self) -> Decimal:
    #     return self.milestones.filter(status="Completed").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    # @property
    # def total_holds_amount(self) -> Decimal:
    #     # expects related_name 'holds' on Hold model
    #     return self.holds.filter(is_active=True).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    # @property
    # def pending(self) -> Decimal:
    #     return (
    #         self.total_available_budget
    #         - (self.payout or Decimal("0.00"))
    #         - self.total_holds_amount
    #         - (self.retention_amount or Decimal("0.00"))
    #         + (self.penalty_amount or Decimal("0.00"))
    #     )

    # @property
    # def budget_utilization_percentage(self) -> Decimal:
    #     if self.total_available_budget == Decimal("0.00"):
    #         return Decimal("0.00")
    #     used = (self.payout or Decimal("0.00")) + (self.retention_amount or Decimal("0.00")) + self.total_holds_amount
    #     return (used / self.total_available_budget) * Decimal("100.00")

    # @property
    # def is_budget_exceeded(self) -> bool:
    #     return self.total_milestones_amount > self.total_available_budget

    # def recalc_payout(self):
    #     total = self.milestones.filter(status="Completed").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    #     self.payout = total

    # def save(self, *args, **kwargs):
    #     try:
    #         self.recalc_payout()
    #     except Exception:
    #         pass
    #     self.budget_exceeded_approved = self.is_budget_exceeded
    #     super().save(*args, **kwargs)
    @property
    def total_available_budget(self) -> Decimal:
        return (self.approved_budget or Decimal("0.00")) + (self.additional_amount or Decimal("0.00"))

    # @property
    # def total_milestones_amount(self) -> Decimal:
    #     if not self.pk:  # avoid querying before object is saved
    #         return Decimal("0.00")
    #     total = self.milestones.aggregate(
    #         total=Coalesce(Sum("amount"), Value(Decimal("0.00")), output_field=DecimalField())
    #     )["total"]
    #     return Decimal(total or 0)
    @property
    def total_milestones_amount(self) -> Decimal:
        if not self.pk:
            return Decimal("0.00")
        total = self.milestones.aggregate(
            total=Coalesce(
                Sum("amount"),
                Value(Decimal("0.00"), output_field=DecimalField(max_digits=16, decimal_places=2)),
                output_field=DecimalField(max_digits=16, decimal_places=2)
            )
        )["total"]
        return Decimal(total or 0)


    @property
    def completed_milestones_amount(self) -> Decimal:
        if not self.pk:
            return Decimal("0.00")
        total = self.milestones.filter(status="Completed").aggregate(
            total=Coalesce(Sum("amount"), Value(Decimal("0.00")), output_field=DecimalField())
        )["total"]
        return Decimal(total or 0)

    @property
    def total_holds_amount(self) -> Decimal:
        if not self.pk:
            return Decimal("0.00")
        total = self.holds.filter(is_active=True).aggregate(
            total=Coalesce(Sum("amount"), Value(Decimal("0.00")), output_field=DecimalField())
        )["total"]
        return Decimal(total or 0)

    @property
    def pending(self) -> Decimal:
        return (
            self.total_available_budget
            - (self.payout or Decimal("0.00"))
            - self.total_holds_amount
            - (self.retention_amount or Decimal("0.00"))
            + (self.penalty_amount or Decimal("0.00"))
        )

    @property
    def budget_utilization_percentage(self) -> Decimal:
        if self.total_available_budget == Decimal("0.00"):
            return Decimal("0.00")
        used = (self.payout or Decimal("0.00")) + (self.retention_amount or Decimal("0.00")) + self.total_holds_amount
        return (used / self.total_available_budget * Decimal("100.00")).quantize(Decimal("0.01"))

    @property
    def is_budget_exceeded(self) -> bool:
        if not self.pk:
            return False
        return self.total_milestones_amount > self.total_available_budget

    def recalc_payout(self):
        if not self.pk:
            return
        total = self.milestones.filter(status="Completed").aggregate(
            total=Coalesce(Sum("amount"), Value(Decimal("0.00")), output_field=DecimalField())
        )["total"] or Decimal("0.00")
        self.payout = total

    def save(self, *args, **kwargs):
        # recalc payout only if object already has a PK
        if self.pk:
            try:
                self.recalc_payout()
            except Exception:
                pass
            self.budget_exceeded_approved = self.is_budget_exceeded
        super().save(*args, **kwargs)

class ProjectPaymentMilestone(models.Model):
    STATUS_CHOICES = [
        ("Planned", "Planned"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("On Hold", "On Hold"),
        ("Cancelled", "Cancelled"),
    ]

    payment_tracking = models.ForeignKey(ProjectPaymentTracking, on_delete=models.CASCADE, related_name="milestones")
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Planned")
    actual_completion_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="milestone_created")
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name="milestone_modified")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "id"]
        verbose_name = "Payment Milestone"
        verbose_name_plural = "Payment Milestones"

    def __str__(self):
        return f"{self.name} - {self.amount} [{self.status}]"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        if not is_new:
            try:
                old_status = ProjectPaymentMilestone.objects.get(pk=self.pk).status
            except ProjectPaymentMilestone.DoesNotExist:
                old_status = None

        super().save(*args, **kwargs)

        if (is_new and self.status == "Completed") or (old_status != "Completed" and self.status == "Completed"):
            tracking = self.payment_tracking
            tracking.recalc_payout()
            tracking.save()


class Hold(models.Model):
    payment_tracking = models.ForeignKey(ProjectPaymentTracking, related_name='holds', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.payment_tracking.save()
        except Exception:
            pass

    def delete(self, *args, **kwargs):
        payment_tracking = self.payment_tracking
        super().delete(*args, **kwargs)
        try:
            payment_tracking.save()
        except Exception:
            pass

    def __str__(self):
        status = "Active" if self.is_active else "Released"
        return f"Hold {self.amount} ({status}) on PaymentTracking #{self.payment_tracking_id}"


class PaymentTransaction(models.Model):
    """
    Records every payout (partial/full). Business logic that updates parent payout should live in services.
    """
    payment_tracking = models.ForeignKey(ProjectPaymentTracking, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now) 
    method = models.CharField(max_length=255, blank=True, null=True)  # e.g., Bank Transfer
    notes = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="transactions_created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"TX #{self.id} - PT#{self.payment_tracking_id} - {self.amount}"


class AdditionalBudgetRequest(models.Model):
    """
    Request / approval workflow for adding to additional_amount on parent PaymentTracking.
    Approve() method atomically applies the change.
    """
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"
    STATUS_REJECTED = "Rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    payment_tracking = models.ForeignKey(ProjectPaymentTracking, on_delete=models.CASCADE, related_name="budget_requests")
    requested_amount = models.DecimalField(max_digits=16, decimal_places=2)
    reason = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="budget_requests_created")
    created_at = models.DateTimeField(auto_now_add=True)

    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="budget_requests_approved")
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Additional Budget Request"
        verbose_name_plural = "Additional Budget Requests"

    def __str__(self):
        return f"AddReq #{self.id} PT#{self.payment_tracking_id} {self.requested_amount} [{self.status}]"

    @transaction.atomic
    def approve(self, approver_user, approval_notes: str = ""):
        if self.status == self.STATUS_APPROVED:
            raise ValidationError("Request already approved.")
        if self.status == self.STATUS_REJECTED:
            raise ValidationError("Request already rejected.")

        # apply to payment tracking atomically
        pt = ProjectPaymentTracking.objects.select_for_update().get(pk=self.payment_tracking_id)
        pt.additional_amount = (pt.additional_amount or Decimal("0.00")) + (self.requested_amount or Decimal("0.00"))
        # If approving budget resolves exceeded budget, keep a flag
        pt.budget_exceeded_approved = pt.is_budget_exceeded or pt.budget_exceeded_approved
        pt.modified_by = approver_user
        pt.save()

        self.status = self.STATUS_APPROVED
        self.approved_by = approver_user
        self.approved_at = timezone.now()
        self.approval_notes = approval_notes
        self.save()
        return self

    @transaction.atomic
    def reject(self, approver_user, notes: str = ""):
        if self.status != self.STATUS_PENDING:
            raise ValidationError("Only pending requests can be rejected.")
        self.status = self.STATUS_REJECTED
        self.approved_by = approver_user
        self.approved_at = timezone.now()
        self.approval_notes = notes
        self.save()
        return self

# class AuditLog(models.Model):
#     """Generic audit log for key models and fields"""
#     model_name = models.CharField(max_length=255)
#     object_id = models.CharField(max_length=255)   # store PK as string
#     field_name = models.CharField(max_length=255, blank=True, null=True)
#     old_value = models.TextField(blank=True, null=True)
#     new_value = models.TextField(blank=True, null=True)
#     changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     changed_at = models.DateTimeField(auto_now_add=True)
#     note = models.TextField(blank=True, null=True)

#     class Meta:
#         ordering = ["-changed_at"]
#         verbose_name = "Audit Log"
#         verbose_name_plural = "Audit Logs"

#     def __str__(self):
#         return f"{self.model_name}#{self.object_id} {self.field_name} @ {self.changed_at}"


# class Notification(models.Model):
#     """Simple notification that can be sent to users or consumed by async workers."""
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
#     title = models.CharField(max_length=255)
#     message = models.TextField()
#     data = models.JSONField(blank=True, null=True)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"Notif to {self.recipient} - {self.title}"


class Rule(models.Model):
    """
    Lightweight rules engine configuration.
    type: which metric to evaluate (budget_utilization, pending_percentage, completed_milestones)
    operator: gt, gte, lt, lte
    value: numeric threshold
    """
    TYPE_CHOICES = [
        ("budget_utilization", "Budget Utilization (%)"),
        ("pending_percentage", "Pending Percentage (%)"),
        ("completed_milestones", "Completed Milestones Amount"),
    ]

    OP_CHOICES = [("gt", ">"), ("gte", ">="), ("lt", "<"), ("lte", "<=")]

    type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    operator = models.CharField(max_length=4, choices=OP_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rule {self.type} {self.operator} {self.value}"


class PaymentHistory(models.Model):
    """
    Explicit history entries (alternative/complimentary to AuditLog) for payment changes.
    """
    payment_tracking = models.ForeignKey(ProjectPaymentTracking, on_delete=models.CASCADE, related_name="history")
    field_changed = models.CharField(max_length=255)
    prev_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"History PT#{self.payment_tracking_id} {self.field_changed} @ {self.changed_at}"



class BudgetPolicy(models.Model):
    MODE_STRICT = "STRICT"
    MODE_FLEX = "FLEXIBLE"
    MODE_AUTO = "AUTO_ADJUST"

    MODE_CHOICES = [
        (MODE_STRICT, "Strict - block when exceeding approved estimation"),
        (MODE_FLEX, "Flexible - allow but warn/audit"),
        (MODE_AUTO, "Auto Adjust - trim to remaining budget"),
    ]

    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="budget_policy")
    mode = models.CharField(max_length=32, choices=MODE_CHOICES, default=MODE_STRICT)
    warning_threshold_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("80.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{getattr(self.project, 'project_name', self.project_id)} Policy ({self.mode})"


class ChangeRequest(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"
    STATUS_REJECTED = "Rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="change_requests")
    requested_amount = models.DecimalField(max_digits=18, decimal_places=2)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cr_requested")
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="cr_reviewed")
    reviewed_at = models.DateTimeField(null=True, blank=True)

    correlation_id = models.CharField(max_length=128, null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"CR#{self.id} for {getattr(self.project, 'project_name', self.project_id)} - {self.requested_amount}"

    # def approve(self, reviewer_user):
    #     """
    #     Approve CR: create new ProjectEstimation version (incremental) and trigger monitor.
    #     """
    #     from .services import BudgetMonitorService  # local import (avoid cycles)
    #     # local import of ProjectEstimation
    #     from .models import ProjectEstimation  # type: ignore

    #     if self.status != self.STATUS_PENDING:
    #         raise ValueError("Only pending CRs can be approved")

    #     with transaction.atomic():
    #         self.status = self.STATUS_APPROVED
    #         self.reviewed_by = reviewer_user
    #         self.reviewed_at = timezone.now()
    #         self.save(update_fields=["status", "reviewed_by", "reviewed_at", "modified_at"])

    #         latest = ProjectEstimation.objects.filter(project=self.project).order_by("-version", "-created_at").first()

    #         if latest:
    #             version = (latest.version or 1) + 1
    #             base_initial = latest.initial_estimation_amount or Decimal("0.00")
    #             base_approved = latest.approved_amount if latest.approved_amount is not None else base_initial
    #         else:
    #             version = 1
    #             base_initial = Decimal("0.00")
    #             base_approved = Decimal("0.00")

    #         new_approved_amount = (base_approved or Decimal("0.00")) + (self.requested_amount or Decimal("0.00"))

    #         ProjectEstimation.objects.create(
    #             project=self.project,
    #             estimation_date=timezone.now().date(),
    #             estimation_provider=None,
    #             estimation_review=None,
    #             version=version,
    #             initial_estimation_amount=base_initial,
    #             approved_amount=new_approved_amount,
    #             is_approved=True,
    #             purchase_order_status="Received",
    #             created_by=reviewer_user,
    #             modified_by=reviewer_user,
    #         )

    #         # audit + trigger monitor
    #         AuditLog.record(self.project, reviewer_user, "change_request.approved", {
    #             "cr_id": self.id, "requested_amount": str(self.requested_amount), "new_approved_amount": str(new_approved_amount)
    #         })
    #         BudgetMonitorService.monitor_project(self.project)
    # def approve(self, reviewer_user):
    #     """
    #     Approve CR: create new ProjectEstimation version (incremental) and trigger monitor.
    #     """
    #     from .services import BudgetMonitorService  # local import (avoid cycles)
    #     from .models import ProjectEstimation  # type: ignore

    #     # Always refresh from DB to avoid stale status
    #     self.refresh_from_db(fields=["status"])

    #     if str(self.status).strip().lower() != str(self.STATUS_PENDING).lower():
    #         raise ValueError(f"Only pending CRs can be approved (current status={self.status})")

    #     with transaction.atomic():
    #         self.status = self.STATUS_APPROVED
    #         self.reviewed_by = reviewer_user
    #         self.reviewed_at = timezone.now()
    #         self.save(update_fields=["status", "reviewed_by", "reviewed_at", "modified_at"])

    #         latest = ProjectEstimation.objects.filter(
    #             project=self.project
    #         ).order_by("-version", "-created_at").first()

    #         if latest:
    #             version = (latest.version or 1) + 1
    #             base_initial = Decimal(latest.initial_estimation_amount or 0)
    #             base_approved = Decimal(latest.approved_amount or base_initial)
    #         else:
    #             version = 1
    #             base_initial = Decimal("0.00")
    #             base_approved = Decimal("0.00")

    #         new_approved_amount = base_approved + Decimal(self.requested_amount or 0)

    #         ProjectEstimation.objects.create(
    #             project=self.project,
    #             estimation_date=timezone.now().date(),
    #             version=version,
    #             initial_estimation_amount=base_initial,
    #             approved_amount=new_approved_amount,
    #             is_approved=True,
    #             purchase_order_status="Received",
    #             created_by=reviewer_user,
    #             modified_by=reviewer_user,
    #         )
            

    #     AuditLog.record(
    #         self.project,
    #         reviewer_user,
    #         "change_request.approved",
    #         {
    #             "cr_id": self.id,
    #             "requested_amount": str(self.requested_amount),
    #             "new_approved_amount": str(new_approved_amount),
    #         },
    #     )
    #     BudgetMonitorService.monitor_project(self.project)
    def approve(self, reviewer_user):
        """
        Approve CR: create new ProjectEstimation version (incremental) and trigger monitor.
        """
        from .services import BudgetMonitorService
        from .models import ProjectEstimation

        # Refresh from DB
        self.refresh_from_db(fields=["status"])

        if self.status != self.STATUS_PENDING:
            raise ValueError(f"Only pending CRs can be approved (current status={self.status})")

        with transaction.atomic():
            # Mark this CR as approved
            self.status = self.STATUS_APPROVED
            self.reviewed_by = reviewer_user
            self.reviewed_at = timezone.now()
            self.save(update_fields=["status", "reviewed_by", "reviewed_at", "modified_at"])

            # Get latest approved estimation
            latest = ProjectEstimation.objects.filter(
                project=self.project, is_approved=True
            ).order_by("-version", "-created_at").first()

            if latest:
                version = latest.version + 1
                base_initial = Decimal(latest.initial_estimation_amount or 0)
                base_approved = Decimal(latest.approved_amount or base_initial)
            else:
                # First approved version
                version = 1
                base_initial = Decimal("0.00")
                base_approved = Decimal("0.00")

            # New approved amount (incremental)
            new_approved_amount = base_approved + Decimal(self.requested_amount or 0)

            # Mark old versions as not approved
            ProjectEstimation.objects.filter(project=self.project, is_approved=True).update(is_approved=False)

            # Create a new estimation version
            new_estimation = ProjectEstimation.objects.create(
                project=self.project,
                estimation_date=timezone.now().date(),
                version=version,
                initial_estimation_amount=base_initial if version > 1 else Decimal("400000.00"),  # ✅ keep base from v1
                approved_amount=new_approved_amount,
                is_approved=True,
                purchase_order_status="Received",
                created_by=reviewer_user,
                modified_by=reviewer_user,
            )

        # Audit + trigger monitor
        AuditLog.record(
            self.project,
            reviewer_user,
            "change_request.approved",
            {
                "cr_id": self.id,
                "requested_amount": str(self.requested_amount),
                "new_approved_amount": str(new_approved_amount),
            },
        )
        BudgetMonitorService.monitor_project(self.project)

        return new_estimation   # ✅ return the new estimation







    def reject(self, reviewer_user):
        if self.status != self.STATUS_PENDING:
            raise ValueError("Only pending CRs can be rejected")
        self.status = self.STATUS_REJECTED
        self.reviewed_by = reviewer_user
        self.reviewed_at = timezone.now()
        self.save(update_fields=["status", "reviewed_by", "reviewed_at", "modified_at"])
        AuditLog.record(self.project, reviewer_user, "change_request.rejected", {"cr_id": self.id})


class AuditLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="audit_logs", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def record(cls, project, user, action, payload=None):
        try:
            cls.objects.create(project=project, user=user, action=action, payload=payload or {})
        except Exception:
            pass

    def __str__(self):
        return f"{self.action} @ {self.created_at}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    extra = models.JSONField(null=True, blank=True)
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification: {self.title} -> {self.user}"
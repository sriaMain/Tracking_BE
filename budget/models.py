from django.db import models

# Create your models here.
from django.db import models
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
 
# Create your models here.


# class ProjectEstimation(BaseModel):
#     project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name="estimation_project" ,null=True,blank=True)
#     estimation_date = models.DateField()
#     estimation_provider = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="estimation_provider", null=True,blank=True)
#     estimation_review = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="estimation_reviewer", null=True,blank=True)
#     initial_estimation_amount = models.DecimalField(max_digits=12, decimal_places=2)
#     estimation_review_by_client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_reviewer")
#     approved_estimation = models.DecimalField(max_digits=12, decimal_places=2)
#     purchase_order_status = models.CharField(max_length=50, choices=[
#         ('Received', 'Received'),
#         ('Pending', 'Pending'),
#     ], default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="estimation_created_by")
#     modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="estimation_modified_by")

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
        return f"{self.project.project_name} - v{self.version}{status}"


# class ProjectPaymentTracking(BaseModel):
#      COST_TYPE_CHOICES = [
#         ("Manpower", "Manpower"),
#         ("Operation Cost", "Operation Cost"),
#         ("Transport", "Transport"),
#         ("Interest", "Interest"),
#         ("Other", "Other"),
#     ]
#      project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
#      payment_type = models.CharField(max_length=50, choices=COST_TYPE_CHOICES)
#      resource = models.ForeignKey(MasterData, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_payments')
#     #  resource = models.ForeignKey(MasterData, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_payments')
#      other_payment_type = models.CharField(max_length=255, blank=True, null=True)
#      approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
#      additional_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#      payout = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#      pending = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#      hold = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#      hold_reason = models.TextField(blank=True, null=True)
#      created_at = models.DateTimeField(auto_now_add=True)
#      modified_at = models.DateTimeField(auto_now=True)
#      created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payment_tracking_created_by")
#      modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payment_tracking_modified_by")


#         # def recalc_pending(self):
            
#         #     milestones_total = sum(self.milestones.values_list('amount', flat=True))
#         #     self.pending = (self.approved_budget or 0) + (self.additional_amount or 0) - (self.payout or 0) - milestones_total
#         #     self.save()
#      def recalc_pending(self):
#         milestones_total = self.milestones.aggregate(
#             total=Sum('amount')
#         )['total'] or 0

#         self.pending = (
#             (self.approved_budget or 0) +
#             (self.additional_amount or 0) -
#             (self.payout or 0) -
#             milestones_total
#         )
#         self.save(update_fields=['pending'])

#      def __str__(self):
#         if self.payment_type == "Other" and self.other_payment_type:
#             return f"{self.project.name} - {self.other_payment_type}"
#         return f"{self.project.name} - {self.payment_type}"

# class ProjectPaymentMilestone(BaseModel):
#     payment_tracking = models.ForeignKey(ProjectPaymentTracking, on_delete=models.CASCADE, related_name='milestones')
#     name = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     due_date = models.DateField(null=True, blank=True)
#     # status = models.ForeignKey(Lookup, on_delete=models.SET_NULL, null=True, blank=True, related_name='milestone_status')

#     def __str__(self):
#         return f"{self.name} - {self.amount}"


# # class ProjectPaymentTracking(BaseModel):
# #     COST_TYPE_CHOICES = [
# #         ("Manpower", "Manpower"),
# #         ("Operation Cost", "Operation Cost"),
# #         ("Transport", "Transport"),
# #         ("Interest", "Interest"),
# #         ("Other", "Other"),
# #     ]
    
# #     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
# #     payment_type = models.CharField(max_length=50, choices=COST_TYPE_CHOICES)
# #     resource = models.ForeignKey(MasterData, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_payments')
# #     other_payment_type = models.CharField(max_length=255, blank=True, null=True)
# #     approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
# #     additional_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
# #     payout = models.DecimalField(max_digits=12, decimal_places=2, default=0)
# #     pending = models.DecimalField(max_digits=12, decimal_places=2, default=0)
# #     hold = models.DecimalField(max_digits=12, decimal_places=2, default=0)
# #     hold_reason = models.TextField(blank=True, null=True)
    
# #     # New fields for better tracking
# #     is_budget_locked = models.BooleanField(default=False)  # Prevent further changes
# #     budget_exceeded_approved = models.BooleanField(default=False)  # Flag for approval needed
    
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     modified_at = models.DateTimeField(auto_now=True)
# #     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payment_tracking_created_by")
# #     modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payment_tracking_modified_by")

# #     @property
# #     def total_available_budget(self):
# #         """Calculate total available budget"""
# #         return (self.approved_budget or Decimal('0')) + (self.additional_amount or Decimal('0'))
    
# #     @property
# #     def total_milestone_amount(self):
# #         """Calculate sum of all milestone amounts"""
# #         return self.milestones.aggregate(
# #             total=Sum('amount')
# #         )['total'] or Decimal('0')
    
# #     @property
# #     def budget_utilization_percentage(self):
# #         """Calculate budget utilization as percentage"""
# #         if self.total_available_budget == 0:
# #             return Decimal('0')
# #         return (self.total_milestone_amount / self.total_available_budget) * 100
    
# #     @property
# #     def is_budget_exceeded(self):
# #         """Check if milestones exceed available budget"""
# #         return self.total_milestone_amount > self.total_available_budget
    
# #     @property
# #     def budget_variance(self):
# #         """Calculate budget variance (positive = under budget, negative = over budget)"""
# #         return self.total_available_budget - self.total_milestone_amount

# #     def recalc_pending(self):
# #         """Recalculate pending amount based on milestones and payouts"""
# #         milestones_total = self.total_milestone_amount
        
# #         # Pending = Total Budget - Payout - Hold
# #         # This represents amount approved but not yet paid
# #         self.pending = (
# #             self.total_available_budget -
# #             (self.payout or Decimal('0')) -
# #             (self.hold or Decimal('0'))
# #         )
        
# #         # If milestones exceed budget, flag for approval
# #         if self.is_budget_exceeded:
# #             self.budget_exceeded_approved = True
            
# #         self.save(update_fields=['pending', 'budget_exceeded_approved'])

# #     def validate_budget_constraints(self):
# #         """Validate all budget constraints"""
# #         errors = []
        
# #         # 1. Check if total milestones exceed available budget
# #         if self.is_budget_exceeded and not self.budget_exceeded_approved:
# #             errors.append(
# #                 f"Milestone total ({self.total_milestone_amount}) exceeds "
# #                 f"available budget ({self.total_available_budget}). "
# #                 f"Excess: {abs(self.budget_variance)}"
# #             )
        
# #         # 2. Check if payout exceeds available budget
# #         if self.payout > self.total_available_budget:
# #             errors.append(
# #                 f"Payout ({self.payout}) cannot exceed "
# #                 f"total budget ({self.total_available_budget})"
# #             )
        
# #         # 3. Check if payout exceeds completed milestones
# #         completed_milestones = self.milestones.filter(status='Completed').aggregate(
# #         total=Sum('amount')
# #         )['total'] or Decimal('0')

        
# #         if self.payout > completed_milestones:
# #             errors.append(
# #                 f"Payout ({self.payout}) cannot exceed "
# #                 f"completed milestones ({completed_milestones})"
# #             )
        
# #         # 4. Logical validation: payout + pending + hold should not exceed budget
# #         total_allocated = (self.payout or Decimal('0')) + (self.pending or Decimal('0')) + (self.hold or Decimal('0'))
# #         if total_allocated > self.total_available_budget:
# #             errors.append(
# #                 f"Total allocated amount ({total_allocated}) exceeds "
# #                 f"available budget ({self.total_available_budget})"
# #             )
        
# #         return errors

# #     def clean(self):
# #         """Django model validation"""
# #         errors = self.validate_budget_constraints()
# #         if errors:
# #             raise ValidationError(errors)

# #     def save(self, *args, **kwargs):
# #         """Override save to ensure budget validation"""
# #         if not self.budget_exceeded_approved:
# #             self.full_clean()  # This calls clean() method
# #         super().save(*args, **kwargs)

# #     def __str__(self):
# #         status = " [BUDGET EXCEEDED]" if self.is_budget_exceeded else ""
# #         if self.payment_type == "Other" and self.other_payment_type:
# #             return f"{self.project.name} - {self.other_payment_type}{status}"
# #         return f"{self.project.name} - {self.payment_type}{status}"


# # class ProjectPaymentMilestone(BaseModel):
# #     STATUS_CHOICES = [
# #         ("Planned", "Planned"),
# #         ("In Progress", "In Progress"),
# #         ("Completed", "Completed"),
# #         ("On Hold", "On Hold"),
# #         ("Cancelled", "Cancelled"),
# #     ]
    
# #     payment_tracking = models.ForeignKey(ProjectPaymentTracking, on_delete=models.CASCADE, related_name='milestones')
# #     name = models.CharField(max_length=255)
# #     amount = models.DecimalField(max_digits=12, decimal_places=2)
# #     due_date = models.DateField(null=True, blank=True)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Planned")
    
# #     # New fields for better tracking
# #     actual_completion_date = models.DateField(null=True, blank=True)
# #     notes = models.TextField(blank=True, null=True)

# #     def clean(self):
# #         """Validate milestone against payment tracking budget"""
# #         if self.payment_tracking_id:
# #             # Get current milestone total excluding this milestone
# #             current_total = self.payment_tracking.milestones.exclude(
# #                 pk=self.pk if self.pk else None
# #             ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
# #             new_total = current_total + (self.amount or Decimal('0'))
# #             available_budget = self.payment_tracking.total_available_budget
            
# #             if new_total > available_budget and not self.payment_tracking.budget_exceeded_approved:
# #                 raise ValidationError(
# #                     f"Adding this milestone (₹{self.amount}) would exceed "
# #                     f"available budget. Current: ₹{current_total}, "
# #                     f"Available: ₹{available_budget}, "
# #                     f"Shortfall: ₹{new_total - available_budget}"
# #                 )

# #     def save(self, *args, **kwargs):
# #         self.full_clean()
# #         super().save(*args, **kwargs)
# #         # Recalculate parent payment tracking
# #         self.payment_tracking.recalc_pending()

# #     def delete(self, *args, **kwargs):
# #         payment_tracking = self.payment_tracking
# #         super().delete(*args, **kwargs)   
# #         # Recalculate after deletion
# #         payment_tracking.recalc_pending()

# #     def __str__(self):
# #         return f"{self.name} - ₹{self.amount} [{self.status}]"  1111


# # class Estimation(BaseModel):
# #     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='estimations')
# #     estimation_date = models.DateField()
# #     estimation_provider = models.CharField(max_length=255)
# #     estimation_review = models.CharField(max_length=255, blank=True, null=True)
# #     initial_estimation_amount = models.DecimalField(max_digits=12, decimal_places=2)
# #     estimation_review_by_client = models.CharField(max_length=255, blank=True, null=True)
# #     approved_estimation = models.DecimalField(max_digits=12, decimal_places=2)
# #     # purchase_order_status = models.ForeignKey(Lookup, on_delete=models.SET_NULL, null=True, blank=True, related_name='po_status')

# #     def __str__(self):
# #         return f"Estimation for {self.project} - {self.initial_estimation_amount}"


# # class Document(BaseModel):
# #     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
# #     file = models.FileField(upload_to='project_documents/')
# #     description = models.TextField(blank=True, null=True)

# #     # generic relation (optional) to tie a doc to budget, payment etc
# #     # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
# #     object_id = models.PositiveIntegerField(null=True, blank=True)
# #     content_object = GenericForeignKey('content_type', 'object_id')

# #     def __str__(self):
# #         return f"Doc: {self.project} - {self.file.name}"








# # # File size limit in bytes (5 MB here)
# # MAX_FILE_SIZE = 5 * 1024 * 1024
# # ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf', '.docx']

# # def validate_file(file):
# #     ext = os.path.splitext(file.name)[1].lower()
# #     if ext not in ALLOWED_EXTENSIONS:
# #         raise ValidationError(f"File type '{ext}' is not allowed.")
# #     if file.size > MAX_FILE_SIZE:
# #         raise ValidationError("File size exceeds the 5MB limit.")
# # def document_upload_path(instance, filename):
# #     # Save files inside a folder for the related model
# #     return f"uploads/{instance.content_type.model}/{instance.object_id}/{filename}"

# # class Document(models.Model):
# #     # Generic ForeignKey Components
# #     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Table Reference
# #     object_id = models.PositiveIntegerField()  # Row ID in that Table
# #     content_object = GenericForeignKey("content_type", "object_id")

# #     # File & Meta Info
# #     file = models.FileField(upload_to=document_upload_path)
# #     description = models.CharField(max_length=255, blank=True, null=True)

# #     uploaded_at = models.DateTimeField(auto_now_add=True)
# #     uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="documents_uploaded")

# #     def __str__(self):
# #         return f"{self.file.name} -> {self.content_object}"

# # class FinanceTransaction(BaseModel):
# #     CREDIT = 'CR'
# #     DEBIT = 'DR'
# #     TX_CHOICES = ((CREDIT, 'Credit'), (DEBIT, 'Debit'))

# #     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='transactions')
# #     date = models.DateField(default=timezone.now)
# #     transaction_type = models.CharField(max_length=2, choices=TX_CHOICES)
# #     description = models.TextField(blank=True, null=True)
# #     amount = models.DecimalField(max_digits=12, decimal_places=2)
# #     related_payment = models.ForeignKey(ProjectPaymentTracking, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')

# #     def __str__(self):
# #         return f"{self.get_transaction_type_display()} {self.amount} - {self.project}"




# # class ProjectReports:
# #     """Helper class with static methods to compute aggregates for a project."""

# #     @staticmethod
# #     def compute_profit_loss(project: Project):
# #         # naive calculation: profit = approved_estimation - actual_cost - payout
# #         estimations = project.estimations.all()
# #         budgets = project.budgets.all()
# #         transactions = project.transactions.all()

# #         estimated_submitted = estimations.aggregate(total=models.Sum('initial_estimation_amount'))['total'] or 0
# #         estimated_approved = estimations.aggregate(total=models.Sum('approved_estimation'))['total'] or 0
# #         approved_budget_cost = budgets.aggregate(total=models.Sum('approved_budget'))['total'] or 0
# #         actual_cost = budgets.aggregate(total=models.Sum('actual_cost'))['total'] or 0
# #         payout = project.payments.aggregate(total=models.Sum('payout'))['total'] or 0
# #         pending = project.payments.aggregate(total=models.Sum('pending'))['total'] or 0

# #         profit_amount = (estimated_approved or 0) - (actual_cost or 0) - (payout or 0)

# #         return {
# #             'estimated_submitted': estimated_submitted,
# #             'estimated_approved': estimated_approved,
# #             'approved_budget_cost': approved_budget_cost,
# #             'actual_cost': actual_cost,
# #             'payout': payout,
# #             'pending': pending,
# #             'profit_amount': profit_amount,
# #         }



# # # from django.db.models.signals import post_save
# # # from django.dispatch import receiver

# # # @receiver(post_save, sender=ProjectBudget)
# # # def create_initial_budget_version(sender, instance, created, **kwargs):
# # #     if created:
# # #         ProjectBudgetVersion.objects.create(
# # #             budget=instance,
# # #             version_number=1,
# # #             estimation_budget=instance.estimation_budget,
# # #             approved_budget=instance.approved_budget,
# # #             change_reason='Initial version'
# # #         )

# # class ProjectBudget(models.Model):
# #     # project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
# #     resource = models.ForeignKey("masterdata.MasterData", on_delete=models.SET_NULL, null=True, blank=True, related_name='budget_resources')
# #     # resource_type = models.ForeignKey(Lookup, on_delete=models.SET_NULL, null=True, blank=True, related_name='budget_types')
# #     estimation_budget = models.DecimalField(max_digits=12, decimal_places=2)
# #     approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
# #     actual_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
# #     reason_for_increase = models.TextField(blank=True, null=True)
# #     created_by = models.ForeignKey(
# #         User,
# #         on_delete=models.SET_NULL,
# #         null=True,
# #         related_name="project_creation_projectbudget_created"  
# #     ) 
# #     modified_by = models.ForeignKey(
# #         User,
# #         on_delete=models.SET_NULL, 
# #         null=True,
# #         related_name="project_creation_projectbudget_modified"  
# #     )
# #     project = models.ForeignKey(
# #         Project,
# #         on_delete=models.CASCADE,
# #         related_name="budget_project_budgets"  )


# #     def __str__(self):
# #         return f"Budget: {self.project} - {self.resource}"


# # class ProjectBudgetVersion(BaseModel):
# #     budget = models.ForeignKey(ProjectBudget, on_delete=models.CASCADE, related_name='versions')
# #     version_number = models.PositiveIntegerField()
# #     estimation_budget = models.DecimalField(max_digits=12, decimal_places=2)
# #     approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
# #     change_reason = models.TextField(blank=True, null=True)

# #     class Meta:
# #         unique_together = (('budget', 'version_number'),)

# #     def __str__(self):
# #         return f"v{self.version_number} - {self.budget}"



from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ValidationError
from masterdata.models import MasterData

# Prefer importing Project from your project_creation app.
# If you DO NOT have a separate Project model, uncomment the local Project class below.
try:
    from project_creation.models import Project
except Exception:
    # If your project does not have project_creation app, uncomment and use the local Project model:
    # class Project(models.Model):
    #     project_name = models.CharField(max_length=255, unique=True)
    #     created_at = models.DateTimeField(auto_now_add=True)
    #
    #     def __str__(self):
    #         return self.project_name
    raise


CURRENCY_CHOICES = [
    ("INR", "Indian Rupee"),
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
]




class ProjectPaymentTracking(models.Model):
    """
    Core payment tracking. All amounts are stored as Decimal fields (currency-aware field can be extended).
    Business calculations (pending, totals) are exposed as properties so UI/serializers can use them.
    """
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

    # Budgets & allocations
    approved_budget = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))
    additional_amount = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))

    # Running amounts
    payout = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))   # cumulative paid
    hold = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))
    hold_reason = models.TextField(blank=True, null=True)

    retention_amount = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))
    penalty_amount = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal("0.00"))

    # Controls
    is_budget_locked = models.BooleanField(default=False)
    budget_exceeded_approved = models.BooleanField(default=False)

    # Audit
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="payment_created")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="payment_modified")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project Payment Tracking"
        verbose_name_plural = "Project Payment Trackings"

    def __str__(self):
        return f"{self.project.project_name} - {self.payment_type} (#{self.id})"

    @property
    def total_available_budget(self) -> Decimal:
        """Approved + additional (only approved additionals should update this field via workflow)."""
        return (self.approved_budget or Decimal("0.00")) + (self.additional_amount or Decimal("0.00"))

    @property
    def total_milestones_amount(self) -> Decimal:
        """Sum of all milestones (planned amounts)."""
        return self.milestones.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    @property
    def completed_milestones_amount(self) -> Decimal:
        """Sum of all completed milestone amounts."""
        return self.milestones.filter(status="Completed").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    @property
    def pending(self) -> Decimal:
        """
        Pending funds that can still be allocated/paid.
        Formula: total_available_budget - payout - hold - retention + penalty
        (penalty_amount can be positive or negative depending on your business)
        """
        return self.total_available_budget - (self.payout or Decimal("0.00")) - (self.hold or Decimal("0.00")) - (self.retention_amount or Decimal("0.00")) + (self.penalty_amount or Decimal("0.00"))

    @property
    def budget_utilization_percentage(self) -> Decimal:
        if self.total_available_budget == Decimal("0.00"):
            return Decimal("0.00")
        return (self.total_milestones_amount / self.total_available_budget) * Decimal("100.00")

    @property
    def is_budget_exceeded(self) -> bool:
        return self.total_milestones_amount > self.total_available_budget

    def recalc_and_save(self):
        """
        Helper to force-save (useful if you programmatically update related models and want derived fields recalculated).
        Note: derived fields are properties — nothing to persist, but you might want this hook for side effects later.
        """
        # Example side-effect: if budget not exceeded, clear flag
        if not self.is_budget_exceeded and self.budget_exceeded_approved:
            self.budget_exceeded_approved = False
            self.save(update_fields=["budget_exceeded_approved"])


class ProjectPaymentMilestone(models.Model):
    """
    Milestones can be planned and when completed they enable payouts.
    By default, milestone creation can be subject to budget checks (service layer or clean()).
    """
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

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="milestone_created")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="milestone_modified")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "id"]
        verbose_name = "Payment Milestone"
        verbose_name_plural = "Payment Milestones"

    def __str__(self):
        return f"{self.name} - {self.amount} [{self.status}]"

    def clean(self):
        """
        Optional model-level validation: ensure milestones don't exceed budget unless explicitly approved.
        You can choose to enforce budget checks in the service layer instead — that's often cleaner.
        """
        if not self.payment_tracking_id:
            return

        # Calculate current total excluding this milestone (for updates)
        existing_total = self.payment_tracking.milestones.exclude(pk=self.pk if self.pk else None).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        new_total = existing_total + (self.amount or Decimal("0.00"))
        available = self.payment_tracking.total_available_budget

        if new_total > available and not self.payment_tracking.budget_exceeded_approved:
            raise ValidationError(
                f"Adding this milestone (₹{self.amount}) would exceed available budget. "
                f"Current: ₹{existing_total}, Available: ₹{available}, Shortfall: ₹{new_total - available}"
            )


class PaymentTransaction(models.Model):
    """
    Records every payout (partial/full). Business logic that updates parent payout should live in services.
    """
    payment_tracking = models.ForeignKey(ProjectPaymentTracking, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now) 
    method = models.CharField(max_length=255, blank=True, null=True)  # e.g., Bank Transfer
    notes = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="transactions_created")
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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="budget_requests_created")
    created_at = models.DateTimeField(auto_now_add=True)

    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="budget_requests_approved")
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


class AuditLog(models.Model):
    """Generic audit log for key models and fields"""
    model_name = models.CharField(max_length=255)
    object_id = models.CharField(max_length=255)   # store PK as string
    field_name = models.CharField(max_length=255, blank=True, null=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-changed_at"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"{self.model_name}#{self.object_id} {self.field_name} @ {self.changed_at}"


class Notification(models.Model):
    """Simple notification that can be sent to users or consumed by async workers."""
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notif to {self.recipient} - {self.title}"


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
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"History PT#{self.payment_tracking_id} {self.field_changed} @ {self.changed_at}"

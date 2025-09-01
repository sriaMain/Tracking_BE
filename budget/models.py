from django.db import models

# Create your models here.
from django.db import models
from project_creation.models import Project
# from masterdata.models import MasterData

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
 
# Create your models here.


class ProjectEstimation(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name="estimation_project" ,null=True,blank=True)
    estimation_date = models.DateField()
    estimation_provider = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="estimation_provider", null=True,blank=True)
    estimation_review = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="estimation_reviewer", null=True,blank=True)
    initial_estimation_amount = models.DecimalField(max_digits=12, decimal_places=2)
    estimation_review_by_client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_reviewer")
    approved_estimation = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_order_status = models.CharField(max_length=50, choices=[
        ('Received', 'Received'),
        ('Pending', 'Pending'),
    ], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="estimation_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="estimation_modified_by")


    

class ProjectPaymentTracking(BaseModel):
     COST_TYPE_CHOICES = [
        ("Manpower", "Manpower"),
        ("Operation Cost", "Operation Cost"),
        ("Transport", "Transport"),
        ("Interest", "Interest"),
        ("Other", "Other"),
    ]
     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
     payment_type = models.CharField(max_length=50, choices=COST_TYPE_CHOICES)
     resource = models.ForeignKey(MasterData, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_payments')
    #  resource = models.ForeignKey(MasterData, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_payments')
     other_payment_type = models.CharField(max_length=255, blank=True, null=True)
     approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
     additional_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
     payout = models.DecimalField(max_digits=12, decimal_places=2, default=0)
     pending = models.DecimalField(max_digits=12, decimal_places=2, default=0)
     hold = models.DecimalField(max_digits=12, decimal_places=2, default=0)
     hold_reason = models.TextField(blank=True, null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     modified_at = models.DateTimeField(auto_now=True)
     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payment_tracking_created_by")
     modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payment_tracking_modified_by")


        # def recalc_pending(self):
            
        #     milestones_total = sum(self.milestones.values_list('amount', flat=True))
        #     self.pending = (self.approved_budget or 0) + (self.additional_amount or 0) - (self.payout or 0) - milestones_total
        #     self.save()
     def recalc_pending(self):
        milestones_total = self.milestones.aggregate(
            total=Sum('amount')
        )['total'] or 0

        self.pending = (
            (self.approved_budget or 0) +
            (self.additional_amount or 0) -
            (self.payout or 0) -
            milestones_total
        )
        self.save(update_fields=['pending'])

     def __str__(self):
        if self.payment_type == "Other" and self.other_payment_type:
            return f"{self.project.name} - {self.other_payment_type}"
        return f"{self.project.name} - {self.payment_type}"

class ProjectPaymentMilestone(BaseModel):
    payment_tracking = models.ForeignKey(ProjectPaymentTracking, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    # status = models.ForeignKey(Lookup, on_delete=models.SET_NULL, null=True, blank=True, related_name='milestone_status')

    def __str__(self):
        return f"{self.name} - {self.amount}"


# class Estimation(BaseModel):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='estimations')
#     estimation_date = models.DateField()
#     estimation_provider = models.CharField(max_length=255)
#     estimation_review = models.CharField(max_length=255, blank=True, null=True)
#     initial_estimation_amount = models.DecimalField(max_digits=12, decimal_places=2)
#     estimation_review_by_client = models.CharField(max_length=255, blank=True, null=True)
#     approved_estimation = models.DecimalField(max_digits=12, decimal_places=2)
#     # purchase_order_status = models.ForeignKey(Lookup, on_delete=models.SET_NULL, null=True, blank=True, related_name='po_status')

#     def __str__(self):
#         return f"Estimation for {self.project} - {self.initial_estimation_amount}"


# class Document(BaseModel):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
#     file = models.FileField(upload_to='project_documents/')
#     description = models.TextField(blank=True, null=True)

#     # generic relation (optional) to tie a doc to budget, payment etc
#     # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
#     object_id = models.PositiveIntegerField(null=True, blank=True)
#     content_object = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):
#         return f"Doc: {self.project} - {self.file.name}"








# # File size limit in bytes (5 MB here)
# MAX_FILE_SIZE = 5 * 1024 * 1024
# ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf', '.docx']

# def validate_file(file):
#     ext = os.path.splitext(file.name)[1].lower()
#     if ext not in ALLOWED_EXTENSIONS:
#         raise ValidationError(f"File type '{ext}' is not allowed.")
#     if file.size > MAX_FILE_SIZE:
#         raise ValidationError("File size exceeds the 5MB limit.")
# def document_upload_path(instance, filename):
#     # Save files inside a folder for the related model
#     return f"uploads/{instance.content_type.model}/{instance.object_id}/{filename}"

# class Document(models.Model):
#     # Generic ForeignKey Components
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Table Reference
#     object_id = models.PositiveIntegerField()  # Row ID in that Table
#     content_object = GenericForeignKey("content_type", "object_id")

#     # File & Meta Info
#     file = models.FileField(upload_to=document_upload_path)
#     description = models.CharField(max_length=255, blank=True, null=True)

#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="documents_uploaded")

#     def __str__(self):
#         return f"{self.file.name} -> {self.content_object}"

# class FinanceTransaction(BaseModel):
#     CREDIT = 'CR'
#     DEBIT = 'DR'
#     TX_CHOICES = ((CREDIT, 'Credit'), (DEBIT, 'Debit'))

#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='transactions')
#     date = models.DateField(default=timezone.now)
#     transaction_type = models.CharField(max_length=2, choices=TX_CHOICES)
#     description = models.TextField(blank=True, null=True)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     related_payment = models.ForeignKey(ProjectPaymentTracking, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')

#     def __str__(self):
#         return f"{self.get_transaction_type_display()} {self.amount} - {self.project}"




# class ProjectReports:
#     """Helper class with static methods to compute aggregates for a project."""

#     @staticmethod
#     def compute_profit_loss(project: Project):
#         # naive calculation: profit = approved_estimation - actual_cost - payout
#         estimations = project.estimations.all()
#         budgets = project.budgets.all()
#         transactions = project.transactions.all()

#         estimated_submitted = estimations.aggregate(total=models.Sum('initial_estimation_amount'))['total'] or 0
#         estimated_approved = estimations.aggregate(total=models.Sum('approved_estimation'))['total'] or 0
#         approved_budget_cost = budgets.aggregate(total=models.Sum('approved_budget'))['total'] or 0
#         actual_cost = budgets.aggregate(total=models.Sum('actual_cost'))['total'] or 0
#         payout = project.payments.aggregate(total=models.Sum('payout'))['total'] or 0
#         pending = project.payments.aggregate(total=models.Sum('pending'))['total'] or 0

#         profit_amount = (estimated_approved or 0) - (actual_cost or 0) - (payout or 0)

#         return {
#             'estimated_submitted': estimated_submitted,
#             'estimated_approved': estimated_approved,
#             'approved_budget_cost': approved_budget_cost,
#             'actual_cost': actual_cost,
#             'payout': payout,
#             'pending': pending,
#             'profit_amount': profit_amount,
#         }



# # from django.db.models.signals import post_save
# # from django.dispatch import receiver

# # @receiver(post_save, sender=ProjectBudget)
# # def create_initial_budget_version(sender, instance, created, **kwargs):
# #     if created:
# #         ProjectBudgetVersion.objects.create(
# #             budget=instance,
# #             version_number=1,
# #             estimation_budget=instance.estimation_budget,
# #             approved_budget=instance.approved_budget,
# #             change_reason='Initial version'
# #         )

# class ProjectBudget(models.Model):
#     # project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
#     resource = models.ForeignKey("masterdata.MasterData", on_delete=models.SET_NULL, null=True, blank=True, related_name='budget_resources')
#     # resource_type = models.ForeignKey(Lookup, on_delete=models.SET_NULL, null=True, blank=True, related_name='budget_types')
#     estimation_budget = models.DecimalField(max_digits=12, decimal_places=2)
#     approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
#     actual_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     reason_for_increase = models.TextField(blank=True, null=True)
#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="project_creation_projectbudget_created"  
#     ) 
#     modified_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL, 
#         null=True,
#         related_name="project_creation_projectbudget_modified"  
#     )
#     project = models.ForeignKey(
#         Project,
#         on_delete=models.CASCADE,
#         related_name="budget_project_budgets"  )


#     def __str__(self):
#         return f"Budget: {self.project} - {self.resource}"


# class ProjectBudgetVersion(BaseModel):
#     budget = models.ForeignKey(ProjectBudget, on_delete=models.CASCADE, related_name='versions')
#     version_number = models.PositiveIntegerField()
#     estimation_budget = models.DecimalField(max_digits=12, decimal_places=2)
#     approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
#     change_reason = models.TextField(blank=True, null=True)

#     class Meta:
#         unique_together = (('budget', 'version_number'),)

#     def __str__(self):
#         return f"v{self.version_number} - {self.budget}"


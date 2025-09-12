from rest_framework import serializers
from .models import ProjectEstimation, ProjectPaymentTracking, ProjectPaymentMilestone, ChangeRequest
from project_creation.models import Project, Client
from .models import (ProjectPaymentTracking, ProjectPaymentMilestone, PaymentTransaction,
                     AdditionalBudgetRequest, Notification, Rule, PaymentHistory, AuditLog,Hold,BudgetPolicy,Invoice)
from roles.models import UserRole
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
# class EstimationSerializer(serializers.ModelSerializer):
#     project_name = serializers.SerializerMethodField()
#     estimation_provider_name = serializers.SerializerMethodField()
#     estimation_review_name = serializers.SerializerMethodField()
#     estimation_review_by_client_name = serializers.SerializerMethodField()
#     created_by = serializers.SerializerMethodField()
#     modified_by = serializers.SerializerMethodField()
#     class Meta:
#         model = ProjectEstimation
#         fields = (
#             'id',
#             'project', 'project_name',
#             'estimation_provider', 'estimation_provider_name',
#             'estimation_review', 'estimation_review_name',
#             'estimation_review_by_client', 'estimation_review_by_client_name',
#             'created_at', 'modified_at',
#             'estimation_date',
#             'initial_estimation_amount',
#             'approved_amount',
#             'is_approved',
#             'purchase_order_status',
#             'created_by', 'modified_by',
#         )
#         read_only_fields = ('created_at', 'modified_at')

#     def get_project_name(self, obj):
#         return getattr(obj.project, "project_code", None)

#     def get_estimation_provider_name(self, obj):
#         try:
#             return obj.estimation_provider.user.username
#         except AttributeError:
#             return None

#     def get_estimation_review_name(self, obj):
#         try:
#             return obj.estimation_review.user.username
#         except AttributeError:
#             return None

#     def get_estimation_review_by_client_name(self, obj):
#         return getattr(obj.estimation_review_by_client, "client_name", None)

#     def get_created_by(self, obj):
#         return getattr(obj.created_by, "username", None)

#     def get_modified_by(self, obj):
#         return getattr(obj.modified_by, "username", None)
# class EstimationSerializer(serializers.ModelSerializer):
#     project_name = serializers.SerializerMethodField()
#     estimation_provider_name = serializers.SerializerMethodField()
#     estimation_review_name = serializers.SerializerMethodField()
#     estimation_review_by_client_name = serializers.SerializerMethodField()

#     created_by = serializers.SerializerMethodField()
#     modified_by = serializers.SerializerMethodField()

#     class Meta:
#         model = ProjectEstimation
#         fields = (
#             "id",
#             "project", "project_name",
#             "estimation_provider", "estimation_provider_name",
#             "estimation_review", "estimation_review_name",
#             "estimation_review_by_client", "estimation_review_by_client_name",
#             "created_at", "modified_at",
#             "estimation_date", "initial_estimation_amount",
#             "approved_amount", "is_approved",
#             "purchase_order_status",
#             "created_by", "modified_by",
#             "version"
#         )
#         read_only_fields = ("created_at", "modified_at")

#     def get_project_name(self, obj):
#         return getattr(obj.project, "project_name", None)

#     def get_estimation_provider_name(self, obj):
#         return getattr(obj.estimation_provider.user, "username", None) if obj.estimation_provider else None

#     def get_estimation_review_name(self, obj):
#         return getattr(obj.estimation_review.user, "username", None) if obj.estimation_review else None

#     def get_estimation_review_by_client_name(self, obj):
#         return getattr(obj.estimation_review_by_client, "client_name", None) if obj.estimation_review_by_client else None

#     def get_created_by(self, obj):
#         return getattr(obj.created_by, "username", None)

#     def get_modified_by(self, obj):
#         return getattr(obj.modified_by, "username", None)


# class EstimationSerializer(serializers.ModelSerializer):
#     project_name = serializers.SerializerMethodField()
#     estimation_provider_name = serializers.SerializerMethodField()
#     estimation_review_name = serializers.SerializerMethodField()
#     estimation_review_by_client_name = serializers.SerializerMethodField()
#     created_by_name = serializers.SerializerMethodField()
#     modified_by_name = serializers.SerializerMethodField()

#     class Meta:
#         model = ProjectEstimation
#         fields = (
#             "id", "project", "project_name",
#             "estimation_provider", "estimation_provider_name",
#             "estimation_review", "estimation_review_name",
#             "estimation_review_by_client", "estimation_review_by_client_name",
#             "created_at", "modified_at", "estimation_date",
#             "initial_amount", "additional_amount",
#             "total_amount", "pending_amount",  # 👈 always recalculated
#             "is_approved", "purchase_order_status",
#             "created_by", "created_by_name",
#             "modified_by", "modified_by_name",
#             "version",
#         )
#         read_only_fields = ("pending_amount", "total_amount")

#     def get_project_name(self, obj):
#         return getattr(obj.project, "project_name", None)

#     def get_estimation_provider_name(self, obj):
#         return getattr(obj.estimation_provider.user, "username", None) if obj.estimation_provider else None

#     def get_estimation_review_name(self, obj):
#         return getattr(obj.estimation_review.user, "username", None) if obj.estimation_review else None

#     def get_estimation_review_by_client_name(self, obj):
#         return getattr(obj.estimation_review_by_client, "client_name", None) if obj.estimation_review_by_client else None

#     def get_created_by_name(self, obj):
#         return getattr(obj.created_by, "username", None)

#     def get_modified_by_name(self, obj):
#         return getattr(obj.modified_by, "username", None)

class EstimationSerializer(serializers.ModelSerializer):
    # Related field names
    project_name = serializers.SerializerMethodField()
    estimation_provider_name = serializers.SerializerMethodField()
    estimation_review_name = serializers.SerializerMethodField()
    estimation_review_by_client_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    modified_by_name = serializers.SerializerMethodField()

    # Consistency and summary fields
    is_data_consistent = serializers.SerializerMethodField()
    payment_summary = serializers.SerializerMethodField()
    consistency_issues = serializers.SerializerMethodField()

    class Meta:
        model = ProjectEstimation
        fields = (
            # Basic fields
            "id", "project", "project_name",
            "estimation_provider", "estimation_provider_name",
            "estimation_review", "estimation_review_name",
            "estimation_review_by_client", "estimation_review_by_client_name",

            # Dates and version
            "created_at", "modified_at", "estimation_date", "version",

            # Financial fields
            "initial_amount", "additional_amount",
            "total_amount", "pending_amount", "received_amount",

            # Status fields
            "is_approved", "purchase_order_status",

            # Audit fields
            "created_by", "created_by_name",
            "modified_by", "modified_by_name",

            # Validation fields
            "is_data_consistent", "payment_summary", "consistency_issues",
        )
        read_only_fields = (
            "id", "pending_amount", "total_amount",  
            "is_data_consistent", "payment_summary", "consistency_issues",
            "created_at", "modified_at", "created_by_name", "modified_by_name",
            "project_name", "estimation_provider_name",
            "estimation_review_name", "estimation_review_by_client_name",
        )

    # ====== Related Names ======
    def get_project_name(self, obj):
        return getattr(obj.project, "project_name", None)

    def get_estimation_provider_name(self, obj):
        return getattr(obj.estimation_provider.user, "username", None) if obj.estimation_provider else None

    def get_estimation_review_name(self, obj):
        return getattr(obj.estimation_review.user, "username", None) if obj.estimation_review else None

    def get_estimation_review_by_client_name(self, obj):
        return getattr(obj.estimation_review_by_client, "client_name", None) if obj.estimation_review_by_client else None

    def get_created_by_name(self, obj):
        return getattr(obj.created_by, "username", None)

    def get_modified_by_name(self, obj):
        return getattr(obj.modified_by, "username", None)

    # ====== Consistency & Payment ======
    def get_is_data_consistent(self, obj):
        validation = obj.status_with_validation
        return validation.get('is_consistent')

    def get_consistency_issues(self, obj):
        validation = obj.status_with_validation
        return validation.get('issues')

    def get_payment_summary(self, obj):
        return obj.payment_summary

    # ====== Validation ======
    def validate(self, data):
        """Custom validation for create/update"""
        received_amount = data.get('received_amount', getattr(self.instance, "received_amount", 0))
        initial_amount = data.get('initial_amount', getattr(self.instance, "initial_amount", 0))
        additional_amount = data.get('additional_amount', getattr(self.instance, "additional_amount", 0))
        total_amount = initial_amount + additional_amount

        if received_amount > total_amount:
            raise serializers.ValidationError("Received amount cannot exceed total amount")

        if self.instance:  # Update case
            current_status = self.instance.purchase_order_status
            new_status = data.get('purchase_order_status', current_status)
            if current_status == ProjectEstimation.STATUS_RECEIVED and new_status != ProjectEstimation.STATUS_RECEIVED:
                raise serializers.ValidationError("Cannot change status from 'Received'")

        return data
    def create(self, validated_data):
        instance = super().create(validated_data)

        # Run consistency fix on creation too
        if instance.purchase_order_status == ProjectEstimation.STATUS_RECEIVED:
            instance.received_amount = instance.total_amount
            instance.pending_amount = Decimal("0.00")
            instance.save()

        return instance

    def update(self, instance, validated_data):
        # If client sets status to "Received", enforce amounts
        if validated_data.get("purchase_order_status") == ProjectEstimation.STATUS_RECEIVED:
            instance.received_amount = instance.total_amount
            instance.pending_amount = Decimal("0.00")
            validated_data["received_amount"] = instance.total_amount
            validated_data["pending_amount"] = Decimal("0.00")

        if 'purchase_order_status' in validated_data:
            instance._explicit_status = True

        instance = super().update(instance, validated_data)

        # Ensure save() recalculation runs
        instance.save()
        return instance






# -----------------------------
# Change Request Serializer
# -----------------------------
class ChangeRequestSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    requested_by_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = ChangeRequest
        fields = (
            "id",
            "project",
            "project_name",
            "requested_amount",
            "reason",
            "status",
            "requested_by",
            "requested_by_name",
            "reviewed_by",
            "reviewed_by_name",
            "reviewed_at",
            "created_at",
            "modified_at",
        )
        read_only_fields = ("status", "reviewed_by", "reviewed_at", "created_at", "modified_at")

    def get_project_name(self, obj):
        return getattr(obj.project, "project_name", None)

    def get_requested_by_name(self, obj):
        return getattr(obj.requested_by, "username", None) if obj.requested_by else None

    def get_reviewed_by_name(self, obj):
        return getattr(obj.reviewed_by, "username", None) if obj.reviewed_by else None

class ProjectPaymentMilestoneSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    modified_by = serializers.SerializerMethodField()

    class Meta:
        model = ProjectPaymentMilestone
        fields = [
            "id", "payment_tracking", "name", "amount", "due_date", "status",
            "actual_completion_date", "notes", "created_by", "modified_by",
            "created_at", "modified_at"
        ]
        read_only_fields = ["created_at", "modified_at"]

    def get_created_by(self, obj):
        return getattr(obj.created_by, "username", None)

    def get_modified_by(self, obj):
        return getattr(obj.modified_by, "username", None)

    def validate_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Milestone amount must be positive.")
        return value


class HoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hold
        fields = ['id', 'amount', 'is_active', 'created_at', 'released_at']


# class ProjectPaymentTrackingSerializer(serializers.ModelSerializer):
#     milestones = ProjectPaymentMilestoneSerializer(many=True, read_only=True)
#     total_available_budget = serializers.SerializerMethodField()
#     total_milestones_amount = serializers.SerializerMethodField()
#     completed_milestones_amount = serializers.SerializerMethodField()
#     total_hold_amount = serializers.SerializerMethodField()
#     pending = serializers.SerializerMethodField()
#     budget_utilization_percentage = serializers.SerializerMethodField()
#     holds = HoldSerializer(many=True, read_only=True)
#     created_by = serializers.SerializerMethodField()
#     modified_by = serializers.SerializerMethodField()

#     class Meta:
#         model = ProjectPaymentTracking
#         fields = [
#             "id", "project", "payment_type", "resource", "currency",
#             "approved_budget", "additional_amount",
#             "payout", "retention_amount", "penalty_amount",
#             "total_available_budget", "total_milestones_amount", "completed_milestones_amount",
#             "total_hold_amount", "pending", "budget_utilization_percentage",
#             "is_budget_locked", "budget_exceeded_approved",
#             "created_by", "modified_by", "created_at", "modified_at",
#             "milestones","holds",
#         ]
#         read_only_fields = [
#             "created_at", "modified_at", "total_available_budget", "total_milestones_amount",
#             "completed_milestones_amount", "total_hold_amount", "pending", "budget_utilization_percentage",
#             "milestones","holds",
#         ]

#     def get_total_available_budget(self, obj):
#         return obj.total_available_budget

#     def get_total_milestones_amount(self, obj):
#         return obj.total_milestones_amount

#     def get_completed_milestones_amount(self, obj):
#         return obj.completed_milestones_amount

#     def get_total_hold_amount(self, obj):
#         return obj.total_holds_amount

#     def get_pending(self, obj):
#         return obj.pending

#     def get_budget_utilization_percentage(self, obj):
#         return obj.budget_utilization_percentage

#     def get_created_by(self, obj):
#         return getattr(obj.created_by, "username", None)

#     def get_modified_by(self, obj):
#         return getattr(obj.modified_by, "username", None)

# class ProjectPaymentTrackingSerializer(serializers.ModelSerializer):
#     milestones = ProjectPaymentMilestoneSerializer(many=True, read_only=True)
#     total_available_budget = serializers.SerializerMethodField()
#     total_milestones_amount = serializers.SerializerMethodField()
#     completed_milestones_amount = serializers.SerializerMethodField()
#     total_holds_amount = serializers.SerializerMethodField()  # ✅ fixed naming
#     pending = serializers.SerializerMethodField()
#     budget_utilization_percentage = serializers.SerializerMethodField()
#     holds = HoldSerializer(many=True, read_only=True)
#     created_by = serializers.SerializerMethodField()
#     modified_by = serializers.SerializerMethodField()

#     class Meta:
#         model = ProjectPaymentTracking
#         fields = [
#             "id", "project", "payment_type", "resource", "currency",
#             "approved_budget", "additional_amount",
#             "payout", "retention_amount", "penalty_amount",
#             "total_available_budget", "total_milestones_amount", "completed_milestones_amount",
#             "total_holds_amount", "pending", "budget_utilization_percentage",  # ✅ fixed
#             "is_budget_locked", "budget_exceeded_approved",
#             "created_by", "modified_by", "created_at", "modified_at",
#             "milestones", "holds",
#         ]
#         read_only_fields = [
#             "created_at", "modified_at", "total_available_budget", "total_milestones_amount",
#             "completed_milestones_amount", "total_holds_amount", "pending", "budget_utilization_percentage",
#             "milestones", "holds",
#         ]

#     def get_total_available_budget(self, obj):
#         return obj.total_available_budget

#     def get_total_milestones_amount(self, obj):
#         return obj.total_milestones_amount

#     def get_completed_milestones_amount(self, obj):
#         return obj.completed_milestones_amount

#     def get_total_holds_amount(self, obj):  # ✅ fixed
#         return obj.total_holds_amount

#     def get_pending(self, obj):
#         return obj.pending

#     def get_budget_utilization_percentage(self, obj):
#         return obj.budget_utilization_percentage

#     def get_created_by(self, obj):
#         return getattr(obj.created_by, "username", None)

#     def get_modified_by(self, obj):
#         return getattr(obj.modified_by, "username", None)   1111111

from decimal import Decimal
from rest_framework import serializers

class ProjectPaymentTrackingSerializer(serializers.ModelSerializer):
    milestones = ProjectPaymentMilestoneSerializer(many=True, read_only=True)
    holds = HoldSerializer(many=True, read_only=True)

    total_available_budget = serializers.SerializerMethodField()
    total_milestones_amount = serializers.SerializerMethodField()
    completed_milestones_amount = serializers.SerializerMethodField()
    total_holds_amount = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()
    budget_utilization_percentage = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    modified_by = serializers.SerializerMethodField()

    class Meta:
        model = ProjectPaymentTracking
        fields = [
            "id", "project", "payment_type", "resource", "currency",
            "approved_budget", "additional_amount",
            "payout", "retention_amount", "penalty_amount",
            "total_available_budget", "total_milestones_amount", "completed_milestones_amount",
            "total_holds_amount", "pending", "budget_utilization_percentage",
            "is_budget_locked", "budget_exceeded_approved",
            "created_by", "modified_by", "created_at", "modified_at",
            "milestones", "holds",
        ]
        read_only_fields = [
            "created_at", "modified_at", "total_available_budget", "total_milestones_amount",
            "completed_milestones_amount", "total_holds_amount", "pending", "budget_utilization_percentage",
            "milestones", "holds",
        ]

    # --- Computed fields ---
    # def get_total_available_budget(self, obj):
    #     return Decimal(obj.approved_budget or 0) - Decimal(obj.payout or 0)

    # def get_total_milestones_amount(self, obj):
    #     total = sum([Decimal(m.amount or 0) for m in getattr(obj, 'milestones', [])])
    #     return total

    # def get_completed_milestones_amount(self, obj):
    #     total = sum([Decimal(m.amount or 0) for m in getattr(obj, 'milestones', []) if m.is_completed])
    #     return total

    # def get_total_holds_amount(self, obj):
    #     total = sum([Decimal(h.amount or 0) for h in getattr(obj, 'holds', [])])
    #     return total

    # def get_pending(self, obj):
    #     pending = (Decimal(obj.approved_budget or 0) + Decimal(obj.additional_amount or 0)) \
    #               - Decimal(obj.payout or 0) - Decimal(obj.retention_amount or 0) - Decimal(obj.penalty_amount or 0)
    #     return pending

    # def get_budget_utilization_percentage(self, obj):
    #     approved = Decimal(obj.approved_budget or 0)
    #     payout = Decimal(obj.payout or 0)
    #     if approved == 0:
    #         return Decimal("0.00")
    #     return (payout / approved * 100).quantize(Decimal("0.01"))

    # def get_created_by(self, obj):
    #     return getattr(obj.created_by, "username", None)

    # def get_modified_by(self, obj):
    #     return getattr(obj.modified_by, "username", None)
    def get_total_available_budget(self, obj):
        return obj.total_available_budget

    def get_total_milestones_amount(self, obj):
        return obj.total_milestones_amount

    def get_completed_milestones_amount(self, obj):
        return obj.completed_milestones_amount

    def get_total_holds_amount(self, obj):
        return obj.total_holds_amount

    def get_pending(self, obj):
        return obj.pending

    def get_budget_utilization_percentage(self, obj):
        return obj.budget_utilization_percentage

    def get_created_by(self, obj):
        return getattr(obj.created_by, "username", None)

    def get_modified_by(self, obj):
        return getattr(obj.modified_by, "username", None)


class ProjectPaymentTrackingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPaymentTracking
        fields = "__all__"
        extra_kwargs = {
            "project": {"required": False},
            "payment_type": {"required": False},
        }

            
class ProfitLossSerializer(serializers.Serializer):
    estimated_submitted = serializers.DecimalField(max_digits=16, decimal_places=2)
    estimated_approved = serializers.DecimalField(max_digits=16, decimal_places=2)
    project_cost_approved_budget = serializers.DecimalField(max_digits=16, decimal_places=2)
    project_cost_actuals = serializers.DecimalField(max_digits=16, decimal_places=2)
    payout = serializers.DecimalField(max_digits=16, decimal_places=2)
    pending = serializers.DecimalField(max_digits=16, decimal_places=2)

    # New fields
    profit = serializers.SerializerMethodField()
    loss = serializers.SerializerMethodField()
    warning = serializers.SerializerMethodField()

    def get_profit(self, obj):
        # profit = estimated_approved - project_cost_actuals (if positive)
        profit_value = Decimal(obj['estimated_approved']) - Decimal(obj['project_cost_actuals'])
        return profit_value if profit_value > 0 else Decimal("0.00")

    def get_loss(self, obj):
        # loss = project_cost_actuals - estimated_approved (if positive)
        loss_value = Decimal(obj['project_cost_actuals']) - Decimal(obj['estimated_approved'])
        return loss_value if loss_value > 0 else Decimal("0.00")

    def get_warning(self, obj):
        if Decimal(obj['project_cost_approved_budget']) > Decimal(obj['estimated_approved']):
            diff = Decimal(obj['project_cost_approved_budget']) - Decimal(obj['estimated_approved'])
            return f"Project cost exceeds approved estimate by {diff}. Consider a ChangeRequest."
        return None

            # Instead of blocking, attach warning


class PaymentTransactionSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PaymentTransaction
        fields = ["id", "payment_tracking", "amount", "transaction_date", "method", "notes", "created_by", "created_at"]
        read_only_fields = ["created_at"]

class AdditionalBudgetRequestSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    approved_by = serializers.SerializerMethodField()
    approved_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = AdditionalBudgetRequest
        # fields = ["id", "payment_tracking", "requested_amount", "reason", "status", "created_by", "created_at", "approved_by", "approved_at", "approval_notes"]
        fields= '__all__'
        read_only_fields = ["status", "created_at", "approved_by", "approved_at", "approval_notes"]

    def get_approved_by(self, obj):
        return obj.approved_by.username if obj.approved_by else None

    def validate_requested_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Requested amount must be positive.")
        return value
    

# class ChangeRequestSerializer(serializers.ModelSerializer):
#     project_name = serializers.CharField(source="project.project_name", read_only=True)
#     requested_by_name = serializers.CharField(source="requested_by.username", read_only=True)
#     reviewed_by_name = serializers.CharField(source="reviewed_by.username", read_only=True)

#     class Meta:
#         model = ChangeRequest
#         fields = [
#             "id",
#             "project_name",
#             "requested_amount",
#             "reason",
#             "status",
#             "requested_by_name",
#             "reviewed_by_name",
#             "reviewed_at",
#             "created_at",
#             "modified_at",
#         ]

# class ChangeRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChangeRequest
#         fields = "__all__"
#         read_only_fields = ("status", "reviewed_by", "reviewed_at", "created_at", "modified_at")



class BudgetPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetPolicy
        fields = "__all__"
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = "__all__"


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = "__all__"


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.project_name", read_only=True)
    client_name = serializers.CharField(source="project.client.name", read_only=True)
    estimation_summary = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "id", "invoice_number", "invoice_date", "due_date",
            "amount", "status", "notes", "pdf_file",
            "project", "project_name", "client_name", "estimation", "estimation_summary",
            "created_at", "modified_at"
        ]
        read_only_fields = ["invoice_number", "pdf_file", "status"]

    def get_estimation_summary(self, obj):
        return {
            "total_amount": obj.estimation.total_amount,
            "received_amount": obj.estimation.received_amount,
            "pending_amount": obj.estimation.pending_amount,
            "payment_summary": obj.estimation.payment_summary
        }
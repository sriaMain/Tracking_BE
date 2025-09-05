from rest_framework import serializers
from .models import ProjectEstimation, ProjectPaymentTracking, ProjectPaymentMilestone
from project_creation.models import Project, Client
from roles.models import UserRole
from django.db.models import Sum
class EstimationSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    estimation_provider_name = serializers.SerializerMethodField()
    estimation_review_name = serializers.SerializerMethodField()
    estimation_review_by_client_name = serializers.SerializerMethodField()

    created_by = serializers.CharField(read_only=True)    
    modified_by = serializers.CharField(read_only=True)

    class Meta:
        model = ProjectEstimation
        fields = (
            'id',
            'project', 'project_name',
            'estimation_provider', 'estimation_provider_name',
            'estimation_review', 'estimation_review_name',
            'estimation_review_by_client', 'estimation_review_by_client_name',
            'created_at', 'modified_at',
            'estimation_date', 'initial_estimation_amount',
            'purchase_order_status',
            'created_by', 'modified_by',
        )
        read_only_fields = ('created_at', 'modified_at')

    def get_project_name(self, obj):
        return obj.project.project_code if obj.project else None

    def get_estimation_provider_name(self, obj):
        return obj.estimation_provider.user.username if obj.estimation_provider else None

    def get_estimation_review_name(self, obj):
        return obj.estimation_review.user.username if obj.estimation_review else None

    def get_estimation_review_by_client_name(self, obj):
        return obj.estimation_review_by_client.client_name if obj.estimation_review_by_client else None

   
   





class ProfitLossSerializer(serializers.Serializer):
    estimated_submitted = serializers.DecimalField(max_digits=12, decimal_places=2)
    estimated_approved = serializers.DecimalField(max_digits=12, decimal_places=2)
    project_cost_approved_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    project_cost_actuals = serializers.DecimalField(max_digits=12, decimal_places=2)
    payout = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit_loss = serializers.DecimalField(max_digits=12, decimal_places=2)




from rest_framework import serializers
from decimal import Decimal
from .models import (
    ProjectPaymentTracking, ProjectPaymentMilestone, PaymentTransaction,
    AdditionalBudgetRequest, Notification, Rule, PaymentHistory, AuditLog
)





class ProjectPaymentMilestoneSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    modified_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProjectPaymentMilestone
        fields = [
            "id", "payment_tracking", "name", "amount", "due_date", "status",
            "actual_completion_date", "notes", "created_by", "modified_by",
            "created_at", "modified_at"
        ]
        read_only_fields = ["created_at", "modified_at"]

    def validate_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Milestone amount must be positive.")
        return value
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # Only recalc if milestone is completed
        if validated_data.get("status") == "Completed":
            tracking = instance.payment_tracking
            approved_budget = tracking.approved_budget or Decimal("0.00")
            payout = tracking.payout or Decimal("0.00")

            # Sum of completed milestones
            completed_sum = (
                ProjectPaymentMilestone.objects.filter(
                    payment_tracking=tracking, status="Completed"
                ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
            )

            # Safe updates (only if fields exist in model)
            if hasattr(tracking, "completed_milestones_amount"):
                tracking.completed_milestones_amount = completed_sum

            if hasattr(tracking, "pending"):
                tracking.pending = approved_budget - (payout + completed_sum)

            if hasattr(tracking, "budget_utilization_percentage"):
                tracking.budget_utilization_percentage = (
                    ((payout + completed_sum) / approved_budget) * 100
                    if approved_budget > 0 else Decimal("0.00")
                )

            tracking.save()

        return instance


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
        fields = ["id", "payment_tracking", "requested_amount", "reason", "status", "created_by", "created_at", "approved_by", "approved_at", "approval_notes"]
        read_only_fields = ["status", "created_at", "approved_by", "approved_at", "approval_notes"]

    def get_approved_by(self, obj):
        return obj.approved_by.username if obj.approved_by else None

    def validate_requested_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Requested amount must be positive.")
        return value


class ProjectPaymentTrackingSerializer(serializers.ModelSerializer):
    total_available_budget = serializers.DecimalField(max_digits=16, decimal_places=2, read_only=True)
    pending = serializers.SerializerMethodField()
    total_milestones_amount = serializers.DecimalField(max_digits=16, decimal_places=2, read_only=True)
    completed_milestones_amount = serializers.DecimalField(max_digits=16, decimal_places=2, read_only=True)
    budget_utilization_percentage = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    modified_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProjectPaymentTracking
        fields = [
            "id", "project", "payment_type", "resource", "currency",
            "approved_budget", "additional_amount",
            "payout", "hold", "hold_reason",
            "retention_amount", "penalty_amount",
            "total_available_budget", "total_milestones_amount", "completed_milestones_amount", "pending", "budget_utilization_percentage",
            "is_budget_locked", "budget_exceeded_approved",
            "created_by", "modified_by", "created_at", "modified_at"
        ]
        read_only_fields = ["created_at", "modified_at", "total_available_budget", "total_milestones_amount", "completed_milestones_amount", "pending", "budget_utilization_percentage"]

    # def get_pending(self, obj):
    #     """
    #     Calculate pending funds as:
    #     total_available_budget - sum of completed milestones - hold - retention + penalty
    #     """
    #     completed = obj.completed_milestones_amount or Decimal("0.00")
    #     pending_amount = (obj.total_available_budget or Decimal("0.00")) - completed - (obj.hold or Decimal("0.00")) - (obj.retention_amount or Decimal("0.00")) + (obj.penalty_amount or Decimal("0.00"))
    #     return pending_amount
    def get_pending(self, obj):
        """
        Pending = total budget - payout - (completed - payout if completed > payout else 0)
                - hold - retention + penalty
        Ensures milestones and payout don’t double count.
        """
        completed = obj.completed_milestones_amount or Decimal("0.00")
        payout = obj.payout or Decimal("0.00")
        hold = obj.hold or Decimal("0.00")
        retention = obj.retention_amount or Decimal("0.00")
        penalty = obj.penalty_amount or Decimal("0.00")

        extra_completed = (completed - payout) if completed > payout else Decimal("0.00")
        pending_amount = (obj.total_available_budget or Decimal("0.00")) - payout - extra_completed - hold - retention + penalty
        return pending_amount



class ProjectPaymentTrackingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPaymentTracking
        fields = "__all__"   # ✅ fixed here
        extra_kwargs = {
            "project": {"required": False},
            "payment_type": {"required": False},
        }

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

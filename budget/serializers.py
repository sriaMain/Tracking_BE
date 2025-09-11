from rest_framework import serializers
from .models import ProjectEstimation, ProjectPaymentTracking, ProjectPaymentMilestone, ChangeRequest
from project_creation.models import Project, Client
from .models import ProjectPaymentTracking, ProjectPaymentMilestone, PaymentTransaction,AdditionalBudgetRequest, Notification, Rule, PaymentHistory, AuditLog,Hold,BudgetPolicy
from roles.models import UserRole
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
class EstimationSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    estimation_provider_name = serializers.SerializerMethodField()
    estimation_review_name = serializers.SerializerMethodField()
    estimation_review_by_client_name = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    modified_by = serializers.SerializerMethodField()
    class Meta:
        model = ProjectEstimation
        fields = (
            'id',
            'project', 'project_name',
            'estimation_provider', 'estimation_provider_name',
            'estimation_review', 'estimation_review_name',
            'estimation_review_by_client', 'estimation_review_by_client_name',
            'created_at', 'modified_at',
            'estimation_date',
            'initial_estimation_amount',
            'approved_amount',
            'is_approved',
            'purchase_order_status',
            'created_by', 'modified_by',
        )
        read_only_fields = ('created_at', 'modified_at')

    def get_project_name(self, obj):
        return getattr(obj.project, "project_code", None)

    def get_estimation_provider_name(self, obj):
        try:
            return obj.estimation_provider.user.username
        except AttributeError:
            return None

    def get_estimation_review_name(self, obj):
        try:
            return obj.estimation_review.user.username
        except AttributeError:
            return None

    def get_estimation_review_by_client_name(self, obj):
        return getattr(obj.estimation_review_by_client, "client_name", None)

    def get_created_by(self, obj):
        return getattr(obj.created_by, "username", None)

    def get_modified_by(self, obj):
        return getattr(obj.modified_by, "username", None)


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

class ChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRequest
        fields = "__all__"
        read_only_fields = ("status", "reviewed_by", "reviewed_at", "created_at", "modified_at")



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

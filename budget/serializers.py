from rest_framework import serializers
from .models import ProjectEstimation, ProjectPaymentTracking, ProjectPaymentMilestone
from project_creation.models import Project, Client
from .models import ProjectPaymentTracking, ProjectPaymentMilestone, PaymentTransaction,AdditionalBudgetRequest, Notification, Rule, PaymentHistory, AuditLog,Hold
from roles.models import UserRole
from django.db.models import Sum
from decimal import Decimal
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

class ProjectPaymentTrackingSerializer(serializers.ModelSerializer):
    milestones = ProjectPaymentMilestoneSerializer(many=True, read_only=True)
    total_available_budget = serializers.SerializerMethodField()
    total_milestones_amount = serializers.SerializerMethodField()
    completed_milestones_amount = serializers.SerializerMethodField()
    total_holds_amount = serializers.SerializerMethodField()  # ✅ fixed naming
    pending = serializers.SerializerMethodField()
    budget_utilization_percentage = serializers.SerializerMethodField()
    holds = HoldSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField()
    modified_by = serializers.SerializerMethodField()

    class Meta:
        model = ProjectPaymentTracking
        fields = [
            "id", "project", "payment_type", "resource", "currency",
            "approved_budget", "additional_amount",
            "payout", "retention_amount", "penalty_amount",
            "total_available_budget", "total_milestones_amount", "completed_milestones_amount",
            "total_holds_amount", "pending", "budget_utilization_percentage",  # ✅ fixed
            "is_budget_locked", "budget_exceeded_approved",
            "created_by", "modified_by", "created_at", "modified_at",
            "milestones", "holds",
        ]
        read_only_fields = [
            "created_at", "modified_at", "total_available_budget", "total_milestones_amount",
            "completed_milestones_amount", "total_holds_amount", "pending", "budget_utilization_percentage",
            "milestones", "holds",
        ]

    def get_total_available_budget(self, obj):
        return obj.total_available_budget

    def get_total_milestones_amount(self, obj):
        return obj.total_milestones_amount

    def get_completed_milestones_amount(self, obj):
        return obj.completed_milestones_amount

    def get_total_holds_amount(self, obj):  # ✅ fixed
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
    profit_loss = serializers.DecimalField(max_digits=16, decimal_places=2)


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

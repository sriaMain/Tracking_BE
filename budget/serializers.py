from rest_framework import serializers
from .models import ProjectEstimation, ProjectPaymentTracking, ProjectPaymentMilestone
from project_creation.models import Project, Client
from roles.models import UserRole
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

   
    # def get_accountant(self, obj):
    #     return UserRoleSerializer(obj.accountant).data if obj.accountant else None






# class ProjectPaymentMilestoneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectPaymentMilestone
#         fields = '__all__'


# class MilestoneAmountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectPaymentMilestone
#         fields = ['amount']


# # ✅ Payment tracking serializer
# class ProjectPaymentTrackingSerializer(serializers.ModelSerializer):
#     milestones = MilestoneAmountSerializer(many=True, read_only=True)  # 👈 only amount here

#     class Meta:
#         model = ProjectPaymentTracking
        # fields = '__all__'

# class ProjectPaymentMilestoneSerializer(serializers.ModelSerializer):1111
#     # """Detailed milestone serializer with status"""
#     # class Meta:
#     #     model = ProjectPaymentMilestone
#     #     fields = ['id', 'name', 'amount', 'due_date', 'status', 'actual_completion_date', 'notes']
# # class ProjectPaymentMilestoneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectPaymentMilestone
#         fields = ['id', 'payment_tracking', 'name', 'amount', 'due_date']
#         read_only_fields = ("created_by", "modified_by")

#     # def create(self, validated_data):
#     #     user = self.context['request'].user
#     #     validated_data["created_by"] = user
#     #     validated_data["modified_by"] = user
#     #     return super().create(validated_data)


# class ProjectPaymentTrackingSerializer(serializers.ModelSerializer):
#     """Enhanced payment tracking serializer with budget analysis"""
#     milestones = ProjectPaymentMilestoneSerializer(many=True, read_only=True)
#     total_available_budget = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
#     total_milestone_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
#     budget_utilization_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
#     is_budget_exceeded = serializers.BooleanField(read_only=True)
#     budget_variance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

#     class Meta:
#         model = ProjectPaymentTracking
#         fields = '__all__'

#     def validate(self, data):
#         """Validate payment data during creation/update"""
#         # Create a temporary instance for validation
#         instance = ProjectPaymentTracking(**data)
        
#         # Check budget constraints
#         errors = instance.validate_budget_constraints()
#         if errors and not data.get('budget_exceeded_approved', False):
#             raise serializers.ValidationError({
#                 'budget_errors': errors
#             })
        
#         return data





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
    pending = serializers.DecimalField(max_digits=16, decimal_places=2, read_only=True)
    total_milestones_amount = serializers.DecimalField(max_digits=16, decimal_places=2, read_only=True)
    completed_milestones_amount = serializers.DecimalField( max_digits=16, decimal_places=2, read_only=True)
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

    def validate(self, attrs):
        # Basic validations; heavy business rules live in services.
        approved = attrs.get("approved_budget", getattr(self.instance, "approved_budget", None))
        additional = attrs.get("additional_amount", getattr(self.instance, "additional_amount", None))
        payout = attrs.get("payout", getattr(self.instance, "payout", None))
        hold = attrs.get("hold", getattr(self.instance, "hold", None))

        total_available = (approved or Decimal("0.00")) + (additional or Decimal("0.00"))
        if payout and payout > total_available:
            raise serializers.ValidationError({"payout": "Payout cannot exceed total available budget (approved + additional)."})
        if hold and hold > total_available:
            raise serializers.ValidationError({"hold": "Hold cannot exceed total available budget."})
        return attrs


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

from rest_framework import serializers
from .models import Estimation

class EstimationSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_code', read_only=True)
    estimation_provider_name = serializers.CharField(source='estimation_provider.user.username', read_only=True)
    estimation_review_name = serializers.CharField(source='estimation_review.user.username', read_only=True)
    estimation_review_by_client_name = serializers.CharField(source='estimation_review_by_client.client_name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    modified_by = serializers.CharField(source='modified_by.username', read_only=True)

    class Meta:
        model = Estimation
        fields = (
            'id',
            'project_name',
            'estimation_provider_name',
            'estimation_review_name',
            'estimation_review_by_client_name',
            'created_at',
            'modified_at',
            'is_deleted',
            'deleted_at',
            'estimation_date',
            'initial_estimation_amount',
            'approved_estimation',
            'purchase_order_status',
            'created_by',
            'modified_by',
        )
        read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')

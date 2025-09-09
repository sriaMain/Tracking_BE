from rest_framework import serializers
from django.db.models import Max
from .models import Client, Project, ProjectUser
from organization.serializers import OrganisationSerializer
from roles_creation.serializers import UserRoleSerializer
from roles_creation.models import UserRole
from authentication.models import User
from users.models import MasterData
from .tasks import send_project_status_email


class ClientSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    modified_by_name = serializers.CharField(source='modified_by.username', read_only=True)

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
 


class ProjectSerializer(serializers.ModelSerializer):
    
    # organization = OrganisationSerializer(read_only=True)
    organization = serializers.CharField(source='organization.organisation_name', read_only=True)
    accountant = serializers.SerializerMethodField()

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    client = serializers.StringRelatedField()
    client_name = serializers.CharField(source="client.name", read_only=True)
    
    # project_manager_details = UserRoleSerializer(source="project_manager", read_only=True)
    project_manager = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = [
            'id',
            'project_code',
            'summary',
            'client',
            'client_name',
            'project_manager',
            'accountant',
            'start_date',
            'end_date',
            'estimated_date',
            'priority',
            'status',
            'status_display',
            'organization',
            'project_type',
            'is_active',
            'project_name',
        
        ]
    def get_project_manager(self, obj):
        return obj.project_manager.user.username if obj.project_manager else None
    
    def get_accountant(self, obj):
        return UserRoleSerializer(obj.accountant).data if obj.accountant else None
    
    def update(self, instance, validated_data):
        old_status = instance.status
        instance = super().update(instance, validated_data)  # Updates fields

        # Check if status changed
        if old_status != instance.status:
            recipients = []

            if instance.project_manager and instance.project_manager.user and instance.project_manager.user.email:
                recipients.append(instance.project_manager.user.email)

            admins = User.objects.filter(is_superuser=True).values_list('email', flat=True)
            recipients.extend(admins)

            recipients = list(filter(None, set(recipients)))

            if recipients:
                send_project_status_email(
                    instance.project_name,
                    old_status,
                    instance.status,
                    recipients
                )
        return instance
    

class ProjectUserSerializer(serializers.ModelSerializer):
   

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), write_only=True
    )
    project_details = serializers.SerializerMethodField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    user_details = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ProjectUser
        fields = ['project', 'user', 'assigned_at', 'project_details', 'user_details']

   
    def get_project_details(self, obj):
        return {
            # "id": obj.project.id,
            "name": obj.project.project_name
        }

    def get_user_details(self, obj):
        master_data = MasterData.objects.filter(name_of_resource=obj.user).first()
        module_name = master_data.module.module_name if master_data and master_data.module else None
 
        return {
            # "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email,
            # "module": obj.user.module.name if obj.user.module else None
            "module": module_name
        }



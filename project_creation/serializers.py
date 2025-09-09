

from rest_framework import serializers
from .models import Client, Project, ClientPOC
 
class ClientSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    modified_by_name = serializers.CharField(source='modified_by.username', read_only=True)
 
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
 
class ClientPocSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    modified_by_name = serializers.CharField(source='modified_by.username', read_only=True)
 
    class Meta:
        model = ClientPOC
        fields = '__all__'
        read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')

# class ProjectSerializer(serializers.ModelSerializer):
#     client_company = serializers.CharField(source='client.Client_company', read_only=True)  
#     client_name = serializers.CharField(source='client.client_name', read_only=True)  
#     poc_name = serializers.CharField(source='poc.name', read_only=True)
#     accountant_name = serializers.CharField(source='accountant.user.username', read_only=True)
#     project_manager_name = serializers.CharField(source='project_manager.user.username', read_only=True)
#     organization_name = serializers.CharField(source='organization.organisation_name', read_only=True)
#     created_by = serializers.CharField(source='created_by.username', read_only=True)
#     modified_by = serializers.CharField(source='modified_by.username', read_only=True)

#     class Meta:
#         model = Project
#         fields = (
#             'id', 'project_code', 'summary', 'start_date', 'end_date', 'estimated_date',
#             'priority', 'project_type', 'is_active', 'created_at', 'modified_at',
#             'created_by', 'modified_by',
#             'client_company', 'client_name', 'poc_name',
#             'accountant_name', 'project_manager_name', 'organization_name',
#         )
#         read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by', 'project_code')

#     # def get_project_id(self, obj):
#     #     return f"SI{str(obj.id).zfill(4)}"


# # class IDSerializer(serializers.ModelSerializer):
# #     pattern = serializers.CharField(write_only=True, required=False)
# #     class Meta:
# #         model = ID
# #         fields = ['id', 'project_code', 'name', 'pattern']
# #         read_only_fields = ['project_code']

# #     def create(self, validated_data):
# #         pattern = validated_data.pop('pattern', None)
# #         instance = ID()
# #         instance.name = validated_data['name']
# #         instance.save(pattern=pattern)  # pass pattern into save()
# #         return instance


class ProjectSerializer(serializers.ModelSerializer):
    # Read-only display fields
    client_company = serializers.CharField(source='client.Client_company', read_only=True)
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    poc_name = serializers.CharField(source='poc.name', read_only=True)
    accountant_name = serializers.CharField(source='accountant.user.username', read_only=True)
    project_manager_name = serializers.CharField(source='project_manager.user.username', read_only=True)
    organization_name = serializers.CharField(source='organization.organisation_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    modified_by_name = serializers.CharField(source='modified_by.username', read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'project_code', 'project_name', 'summary', 'start_date', 'end_date', 'estimated_date',
            'priority', 'project_type', 'is_active', 'created_at', 'modified_at',
            'client', 'poc', 'accountant', 'project_manager', 'organization',
            'client_company', 'client_name', 'poc_name',
            'accountant_name', 'project_manager_name', 'organization_name',
            'created_by_name', 'modified_by_name',
        )
        read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by', 'project_code')

    # Validate summary length and dates
    def validate_summary(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Summary must be at least 10 characters long.")
        return value

    # Validate project_name uniqueness (case-insensitive)
    def validate_project_name(self, value):
        value = value.strip()
        qs = Project.objects.filter(project_name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Project name already exists.")
        return value

    # Validate POC, end_date, estimated_date
    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        estimated_date = attrs.get('estimated_date')
        client = attrs.get('client')
        poc = attrs.get('poc')

        if poc and client and poc.client != client:
            raise serializers.ValidationError("POC must belong to the same client as the project.")

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError("End date cannot be earlier than start date.")

        if estimated_date and start_date and estimated_date < start_date:
            raise serializers.ValidationError("Estimated date cannot be before start date.")

        return attrs

# class ProjectSerializer(serializers.ModelSerializer):
#     # Read-only display fields
#     client_company = serializers.CharField(source='client.Client_company', read_only=True)  
#     client_name = serializers.CharField(source='client.client_name', read_only=True)  
#     poc_name = serializers.CharField(source='poc.name', read_only=True)
#     accountant_name = serializers.CharField(source='accountant.user.username', read_only=True)
#     project_manager_name = serializers.CharField(source='project_manager.user.username', read_only=True)
#     organization_name = serializers.CharField(source='organization.organisation_name', read_only=True)
#     created_by_name = serializers.CharField(source='created_by.username', read_only=True)
#     modified_by_name = serializers.CharField(source='modified_by.username', read_only=True)

#     class Meta:
#         model = Project
#         fields = (
#             'id', 'project_code', 'summary', 'start_date', 'end_date', 'estimated_date',
#             'priority', 'project_type', 'is_active', 'created_at', 'modified_at',
            
#             # Foreign keys (for write)
#             'client', 'poc', 'accountant', 'project_manager', 'organization',

#             # Readable display fields (for read)
#             'client_company', 'client_name', 'poc_name',
#             'accountant_name', 'project_manager_name', 'organization_name',
#             'created_by_name', 'modified_by_name',
#         )
#         read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by', 'project_code')

#         # def validate_summary(self, value):
#         #     start_date = self.initial_data.get("start_date")
#         #     end_date = self.initial_data.get("end_date")

#         #     if start_date and end_date and end_date < start_date:
#         #         raise serializers.ValidationError("End date must be after start date.")
#         #     if len(value) < 10:
#         #         raise serializers.ValidationError("Summary must be at least 10 characters long.")
#         #     return value
#     def validate_summary(self, value):
#         start_date = self.initial_data.get("start_date")
#         end_date = self.initial_data.get("end_date")

#         if start_date and end_date and end_date < start_date:
#             raise serializers.ValidationError("End date must be after start date.")
#         if len(value) < 10:
#             raise serializers.ValidationError("Summary must be at least 10 characters long.")
#         return value
#     def validate_project_name(self, value):
#         value = value.strip()
#         qs = Project.objects.filter(project_name__iexact=value)
#         if self.instance:
#             qs = qs.exclude(pk=self.instance.pk)
#         if qs.exists():
#             raise serializers.ValidationError("Project name must be unique.")
#         return value
        

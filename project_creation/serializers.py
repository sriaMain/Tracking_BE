# from rest_framework import serializers
# from .models import Client, Project
# from roles.models import UserRole

# class ClientSerializer(serializers.ModelSerializer):
#     created_by_name = serializers.CharField(source='created_by.username', read_only=True)
#     modified_by_name = serializers.CharField(source='modified_by.username', read_only=True)

#     class Meta:
#         model = Client
#         fields = '__all__'
#         read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')


# class ProjectSerializer(serializers.ModelSerializer):
#     client = serializers.CharField(source='client.client_name', read_only=True)
#     accountant = serializers.SerializerMethodField()
#     project_manager = serializers.SerializerMethodField()
#     created_by = serializers.CharField(source='created_by.username', read_only=True)

#     class Meta:
#         model = Project
#         fields = '__all__'

#     # def get_accountant(self, obj):
#     #     if obj.accountant:
#     #         return {
#     #             # "id": obj.accountant.user_role_id,  # correct PK name
#     #             "user_name": obj.accountant.user.username,
#     #             # "role_name": obj.accountant.role.name
#     #         }
#     #     return None

#     # def get_project_manager(self, obj):
#     #     if obj.project_manager:
#     #         return {
#     #             # "id": obj.project_manager.user_role_id,  # correct PK name
#     #             "user_name": obj.project_manager.user.username,
#     #             # "role_name": obj.project_manager.role.name
#     #         }
#     #     return None

#         read_only_fields = ['project_code']  # stop request from setting it

#     def create(self, validated_data):
#         # Always remove any project_code accidentally sent from frontend
#         validated_data.pop('project_code', None)
#         validated_data['project_code'] = self.generate_project_code()
#         return super().create(validated_data)

#     def generate_project_code(self):
#         from django.db.models import Max
#         import re

#         last_code = Project.objects.aggregate(Max('project_code'))['project_code__max']
#         if last_code:
#             match = re.search(r'(\d+)$', last_code)
#             if match:
#                 last_number = int(match.group(1))
#                 return f"PRJ-2025-{last_number + 1:03d}"
#         return "PRJ-2025-001"

#     def get_accountant(self, obj):
#         if obj.accountant:
#             return {"user_name": obj.accountant.user.username}
#         return None

#     def get_project_manager(self, obj):
#         if obj.project_manager:
#             return {"user_name": obj.project_manager.user.username}
#         return None


from rest_framework import serializers
from .models import Client, Project, ID, ClientPOC
 
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

class ProjectSerializer(serializers.ModelSerializer):
    client_company = serializers.CharField(source='client.Client_company', read_only=True)  
    client_name = serializers.CharField(source='client.client_name', read_only=True)  
    poc_name = serializers.CharField(source='poc.name', read_only=True)
    accountant_name = serializers.CharField(source='accountant.user.username', read_only=True)
    project_manager_name = serializers.CharField(source='project_manager.user.username', read_only=True)
    organization_name = serializers.CharField(source='organization.organisation_name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    modified_by = serializers.CharField(source='modified_by.username', read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'project_code', 'summary', 'start_date', 'end_date', 'estimated_date',
            'priority', 'project_type', 'is_active', 'created_at', 'modified_at',
            'created_by', 'modified_by',
            'client_company', 'client_name', 'poc_name',
            'accountant_name', 'project_manager_name', 'organization_name',
        )
        read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by', 'project_code')

    def get_project_id(self, obj):
        return f"SI{str(obj.id).zfill(4)}"


class IDSerializer(serializers.ModelSerializer):
    pattern = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = ID
        fields = ['id', 'project_code', 'name', 'pattern']
        read_only_fields = ['project_code']

    def create(self, validated_data):
        pattern = validated_data.pop('pattern', None)
        instance = ID()
        instance.name = validated_data['name']
        instance.save(pattern=pattern)  # pass pattern into save()
        return instance

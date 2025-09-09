from .models import Module, MasterData
from rest_framework import serializers
from roles_creation.models import UserRole
from authentication.models import User
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['module_id', 'module_name', 'module_description', 'created_at', 'modified_at']



class MasterDataSerializer(serializers.ModelSerializer):
    user_role_name = serializers.SerializerMethodField()
    # module = serializers.SlugRelatedField(
    #     queryset=Module.objects.all(), 
    #     slug_field='module_name'
    # ) 
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())  # for write
    # module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())  # for write
    # module_name = serializers.CharField(source='module.module_name', read_only=True)
    name_of_resource = serializers.CharField(source='name_of_resource.username', read_only=True)
    class Meta:
        model = MasterData
        fields = '__all__'
        extra_kwargs = {
            'module': {'required': True, 'allow_null': False},
            'name_of_resource': {'required': True, 'allow_null': False},
            'type_of_resource': {'required': True, 'allow_blank': False},
            'contact_details': {'required': True, 'allow_blank': False},
            'pan': {'required': True, 'allow_blank': False},
            'gst': {'required': True, 'allow_blank': False},
            'address': {'required': True, 'allow_blank': False},
            'work_location': {'required': True, 'allow_blank': False},
            'work_type': {'required': True, 'allow_blank': False},
            'experience': {'required': True, 'allow_blank': False},
            'skill_set': {'required': True, 'allow_blank': False},
        }
    def get_user_role_name(self, obj):
        user_role = UserRole.objects.filter(user=obj.name_of_resource).first()
        return user_role.role.name if user_role else None
    def to_representation(self, instance):
        """Return module name instead of ID in response"""
        rep = super().to_representation(instance)
        if instance.module:
            rep['module'] = instance.module.module_name
        # if instance.name_of_resource:
        #     rep['name_of_resource'] = instance.name_of_resource.username
        return rep

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            
        ]
        read_only_fields = ['id', 'username', 'email']
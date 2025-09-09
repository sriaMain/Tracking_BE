from rest_framework import serializers
from .models import Task
from authentication.models import User
from project_creation.models import Project
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
    created_by = serializers.CharField(source='created_by.email', read_only=True)  
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True) 

   
    start_date = serializers.DateField(required=True)
    due_date = serializers.DateField(required=True)
   
    
    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field='project_name'
    )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
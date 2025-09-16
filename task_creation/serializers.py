from rest_framework import serializers
from .models import Task
from authentication.models import User
from project_creation.models import Project
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = "__all__"
#     created_by = serializers.CharField(source='created_by.email', read_only=True)  
#     assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True) 

   
#     start_date = serializers.DateField(required=True)
#     due_date = serializers.DateField(required=True)
#     project_id = serializers.PrimaryKeyRelatedField(
#         queryset=Project.objects.all(),
#         write_only=True,
#         required=True
#     )
    
#     project = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='project_name'
#     )

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

    # def update(self, instance, validated_data):
    #     # Pop project_id and assign it to project FK
    #     project = validated_data.pop('project_id', None)
    #     if project:
    #         instance.project = project

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.email', read_only=True)
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)

    start_date = serializers.DateField(required=True)
    due_date = serializers.DateField(required=True)

    # Input field for create/update
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        write_only=True,
        required=True
    )

    # Output field
    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field='project_name'
    )

    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        project = validated_data.pop('project_id')  # Extract the Project instance
        task = Task.objects.create(project=project, **validated_data)
        return task

    def update(self, instance, validated_data):
        project = validated_data.pop('project_id', None)
        if project:
            instance.project = project

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

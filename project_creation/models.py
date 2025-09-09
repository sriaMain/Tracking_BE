from django.db import models
from authentication.models import User
from django.utils import timezone
from users.models import MasterData
from django.contrib.contenttypes.fields import GenericForeignKey
from authentication.models import BaseModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import re
import os
from django.core.exceptions import ValidationError
from roles_creation.models import UserRole
from .tasks import send_project_status_email
# from .utils import increment_code

class Client(models.Model):
    Client_id = models.AutoField(primary_key=True)
    Client_name = models.CharField(max_length=255)  
    poc_name = models.CharField(max_length=255)
    poc_email = models.EmailField()
    poc_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)    
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client_modified_by')

    def __str__(self):
        return self.Client_name    


class Project(models.Model):
    class StatusChoices(models.TextChoices):
        REQUIREMENTS = "Requirements", "Requirements"          #Initial phase where requirements are gathered, analyzed, and documented.
        Planning = "Planning", "Planning"                      #Defining scope, creating schedules, assigning resources, and planning deliverables.
        DESIGN = "Design", "Design"                            #Creating architecture, UI/UX designs, and technical specifications.        
        DEVELOPMENT = "Development", "Development"             #Actual coding, building, and implementation of planned features.
        # READY_FOR_TEST = "Ready for Test", "Ready for Test"    #Development completed, waiting for QA/testing team to validate functionality.
        TESTING = "Testing", "Testing"                         #Quality assurance phase where the product is tested for bugs, issues, and performance. 
        UAT = "UAT", "UAT"                                     #User Acceptance Testing by end-users to validate the product meets their needs. 
        PRODUCTION = "Production", "Production"                #The project or feature is deployed live for end-users.   
        MAINTENANCE = "Maintenance", "Maintenance"             #Ongoing support, bug fixes, updates, and improvements after launch.   
        REVIEW = "Review", "Review"                            #Work is under peer review, code review, or management approval before moving ahead.   
        COMPLETED = "Completed", "Completed"                   #Work is fully finished, approved, and closed successfully.
        ON_HOLD = "On Hold", "On Hold"                         #Work is paused temporarily due to resource, priority, or dependency issues.     
        CANCELLED = "Cancelled", "Cancelled"                   #Work has been terminated and will not continue further.
    # project_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='projects', null=True, blank=True)
    project_code = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=255)
    # type = models.CharField(max_length=100)
    summary = models.TextField()
    accountant= models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="project_accountant", null=True,blank=True)
    project_manager = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="project_manager", null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    estimated_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium')
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.Planning)
    organization = models.ForeignKey('organization.Organisation', on_delete=models.SET_NULL, null=True, related_name='projects_organization')
    project_type = models.CharField(max_length=50, choices=[('Internal', 'Internal'), ('Client-Based', 'Client-Based')], default='Internal') 
    is_active = models.BooleanField(default=True)  # Soft deletion flag
    created_at = models.DateTimeField(auto_now_add=True)    
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_modified_by') 
    
    def __str__(self):
        return self.project_name   

    
 
# models.py
class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="assigned_users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_projects")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')  # Prevent duplicate assignment

    def __str__(self):
        return f"{self.user.username} -> {self.project.project_name}"




    










from django.db import models
from login.models import User
from django.utils import timezone
# from masterdata.models import MasterData
from login.models import BaseModel
from roles.models import UserRole
from django.core.exceptions import ValidationError
from django.db.models import Max
import re
from organization.models import Organisation
from django.db import transaction


class Client(models.Model):
    client_id = models.BigAutoField(primary_key=True)
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name="clients"
    )
    Client_company= models.CharField(max_length=100, unique=True)
    client_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_modified')

    
    # class Meta:
    #     db_table = "client"
    #     unique_together = ("organisation", "client_company")
    #     indexes = [models.Index(fields=["client_company"])]

    def __str__(self):
        return f"{self.Client_company} ({self.organisation.organisation_name})"

    def __str__(self):
        return self.client_name


class ClientPOC(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="pocs")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='poc_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='poc_modified_by')

    class Meta:
        unique_together = ['client', 'email']
        ordering = ['-is_primary', 'name']  

    def __str__(self):
        return f"{self.name} ({self.client.client_name})"


class Project(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    PROJECT_TYPE_CHOICES = [
        ('Internal', 'Internal'),
        ('Client-Based', 'Client-Based'),
    ]


    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    poc = models.ForeignKey(ClientPOC, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    project_code = models.CharField(max_length=100)
    project_name = models.CharField(max_length=255,unique=True)
    # type = models.CharField(max_length=100)
    summary = models.TextField()
    accountant= models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="project_accountant", null=True,blank=True)
    project_manager = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="project_manager", null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    estimated_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=50,choices=PRIORITY_CHOICES,default='Medium' )
    # company_name = models.CharField(max_length=50)
    organization = models.ForeignKey('organization.Organisation', on_delete=models.SET_NULL, null=True, related_name='projects_organization')
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES,default='Internal') 
    is_active = models.BooleanField(default=True)  # Soft deletion flag
    created_at = models.DateTimeField(auto_now_add=True)    
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_modified_by')    


    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #     if self.poc and self.poc.client != self.client:
    #         raise ValidationError("POC must belong to the same client as the project")
        
    # def clean(self):
    #     if self.end_date < self.start_date:
    #         raise ValidationError("End date cannot be earlier than start date.")
    #     if self.estimated_date and self.start_date and self.estimated_date < self.start_date:
    #         raise ValidationError("Estimated date cannot be before start date.")

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.poc and self.client and self.poc.client != self.client:
            raise ValidationError("POC must belong to the same client as the project")
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")
        if self.estimated_date and self.start_date and self.estimated_date < self.start_date:
            raise ValidationError("Estimated date cannot be before start date.")

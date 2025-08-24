from django.db import models
from login.models import User
from django.utils import timezone
from user_profile.models import MasterData
from login.models import BaseModel
from roles.models import UserRole
from django.core.exceptions import ValidationError
from django.db.models import Max
import re

# class Client(models.Model):
#     client_id = models.AutoField(primary_key=True)
#     client_name = models.CharField(max_length=255)  
#     poc_name = models.CharField(max_length=255)
#     poc_email = models.EmailField()
#     poc_phone = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)    
#     modified_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client_created_by')
#     modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client_modified_by')    

#     def __str__(self):
#         return self.client_name


class Client(models.Model):
    Client_company= models.CharField(max_length=100, unique=True)
    client_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_modified')

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


    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    poc = models.ForeignKey(ClientPOC, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    project_code = models.CharField(max_length=100, unique=True)
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

    def __str__(self):
        return f"{self.project_code} - {self.client.client_name}" 
    def save(self, *args, **kwargs):
        # Step 1: Check if no code already assigned
        if not self.project_code:
            # Step 2: If pattern passed to Project, forward it to ID
            pattern = kwargs.pop("pattern", None)
 
            id_obj = ID(name="project")
            if pattern:
                id_obj.save(pattern=pattern)  # pass pattern to ID model
            else:
                id_obj.save()
 
            # Step 3: Assign generated code to Project
            self.project_code = id_obj.project_code
 
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.poc and self.poc.client != self.client:
            raise ValidationError("POC must belong to the same client as the project")

class IDPattern(models.Model):
    # Example: SI{year}{seq:03d} or SI{seq:05d}
    name = models.CharField(max_length=50, unique=True)  # Pattern name (e.g., "project", "sales")
    pattern = models.CharField(max_length=50)  # Format string
 
    def __str__(self):
        return f"{self.name} -> {self.pattern}"
 

class ID(models.Model):
    project_code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    

    def save(self, *args, **kwargs):
        if not self.project_code:
            # Step 1: Get pattern
            pattern_str = kwargs.pop("pattern", None)
            if not pattern_str:
                pattern_obj = IDPattern.objects.filter(name="project").first()
                pattern_str = pattern_obj.pattern if pattern_obj else "SI{year}{seq:03d}"
 
            # Step 2: Year + build prefix
            year = timezone.now().year
            prefix = pattern_str.split("{")[0]  # everything before first placeholder
 
            # Step 3: Only look at codes that match this pattern
            filter_kwargs = {}
            if "{year}" in pattern_str:
                filter_kwargs["project_code__startswith"] = f"{prefix}{year}"
            else:
                filter_kwargs["project_code__startswith"] = prefix
 
            last_project = ID.objects.filter(**filter_kwargs).order_by('-id').first()
 
            if last_project:
                match = re.search(r'(\d+)$', last_project.project_code)
                last_seq = int(match.group(1)) if match else 0
                seq = last_seq + 1
            else:
                seq = 1
 
            # Step 4: Format project_code
            self.project_code = pattern_str.format(year=year, seq=seq)
 
        super().save(*args, **kwargs)
 
 
 

# class ProjectBudget(BaseModel):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="budgets")
#     resource_name = models.CharField(max_length=255)
#     resource_type = models.CharField(max_length=50)  # e.g., Manpower, Operation Cost
#     estimation_budget = models.DecimalField(max_digits=12, decimal_places=2)
#     approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
#     actual_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     reason_for_increase = models.TextField(blank=True, null=True)

# class PaymentTracking(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="payments")
#     resource_name = models.CharField(max_length=255)
#     resource_type = models.CharField(max_length=50)
#     approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
#     milestone_1 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     milestone_2 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     milestone_3 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     additional_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     payout = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     pending = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     hold = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     hold_reason = models.TextField(blank=True, null=True)

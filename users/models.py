from django.db import models

# Create your models here.
class Module(models.Model):
    module_id = models.BigAutoField(primary_key=True)
    module_name = models.CharField(max_length=255, unique=True)
    module_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.module_name
    

class MasterData(models.Model):
    RESOURCE_TYPE_CHOICES = [
    ('Freelance', 'Freelance'),                 # Independent contractor
    ('Full Time', 'Full Time'),                 # Permanent employee
    ('Part Time', 'Part Time'),                 # Works limited hours
    ('Contract', 'Contract'),                   # Fixed-term contract
    ('Intern', 'Intern'),                       # Temporary training position
    ('Consultant', 'Consultant'),               # Advisory/project-based role
    ('Temporary', 'Temporary'),                 # Short-term employment
    ('Vendor', 'Vendor'),                       # External vendor-provided resource
    ('Outsourced', 'Outsourced'),               # From another company
    ('Apprentice', 'Apprentice'),               # Learning role with mentorship
    ('Other', 'Other'),                     # Any other type not listed
]
    
    WORK_TYPE_CHOICES = [
    ("On-site", "On-site"),                 # Works entirely at company premises
    ("Remote", "Remote"),                   # Works entirely from home or other location
    ("Hybrid", "Hybrid"),                   # Mix of remote and on-site work
    ("Shift-based", "Shift-based"),         # Fixed shifts (morning, night, rotational)
    ("Field Work", "Field Work"),           # Out in the field / customer site
    ("Project-based", "Project-based"),     # Works only for the duration of a project
    ("On-call", "On-call"),                 # Works when needed, flexible hours
    ("Travel-intensive", "Travel-intensive"), # Frequent travel required
    ("Flexible Hours", "Flexible Hours"),   # No fixed schedule
    ("Training", "Training"),               # Currently in training phase
]

    
    # module = models.ForeignKey(Module, on_delete=models.SET_NULL, related_name='master_data')
    name_of_resource = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, related_name='master', null=True, blank=True)
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="resources", null=True, blank=True)
    
    type_of_resource = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES) 
    contact_details = models.CharField(max_length=100, blank=True, null=True)
    pan = models.CharField(max_length=15, blank=True, null=True)
    gst = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    work_location = models.CharField(max_length=100, blank=True, null=True)
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES)
    experience = models.CharField(max_length=50, blank=True, null=True)
    skill_set = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return f"{self.name_of_resource} - {self.module.module_name}"

    # def __str__(self):
    #     name = self.name_of_resource if self.name_of_resource else "No User"
    #     module = self.module.module_name if self.module else "No Module"
    #     return f"{name} - {module}"

    def __str__(self):
        name = self.name_of_resource.username if self.name_of_resource else "No User"  # <- CHANGE THIS
        module = self.module.module_name if self.module else "No Module"
        return f"{name} - {module}"

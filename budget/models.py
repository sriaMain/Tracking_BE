from django.db import models
from project_creation.models import Project
from users.models import MasterData
from authentication.models import User, BaseModel

# Create your models here.
class ProjectBudget(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
    resource = models.ForeignKey(MasterData, on_delete=models.SET_NULL, null=True, blank=True, related_name='budgets')
    # resource_type = models.ForeignKey(Lookup, on_delete=models.SET_NULL, null=True, blank=True, related_name='budget_types')
    estimation_budget = models.DecimalField(max_digits=12, decimal_places=2)
    approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reason_for_increase = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="project_creation_projectbudget_created"  # ✅ unique
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="project_creation_projectbudget_modified"  # ✅ unique
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_creation_project_budgets"  )# ✅ unique


    def __str__(self):
        return f"Budget: {self.project} - {self.resource or self.resource_type}"


class ProjectBudgetVersion(BaseModel):
    budget = models.ForeignKey(ProjectBudget, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    estimation_budget = models.DecimalField(max_digits=12, decimal_places=2)
    approved_budget = models.DecimalField(max_digits=12, decimal_places=2)
    change_reason = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('budget', 'version_number'),)

    def __str__(self):
        return f"v{self.version_number} - {self.budget}"


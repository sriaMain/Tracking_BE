from django.contrib import admin
from .models import Client, Project, ProjectUser

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('Client_name', 'poc_name', 'poc_email')
    search_fields = ('Client_name', 'poc_name', 'poc_email')  # ✅ tuple/list


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_code', 'client', 'accountant', 'project_manager')
    search_fields = ('project_code', 'client__client_name', 'accountant__user__username', 'project_manager__user__username')


@admin.register(ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'assigned_at')
    search_fields = ('project__project_name', 'user__username', 'user__email')
from django.contrib import admin
from .models import Module, MasterData

@admin.register(Module)
# @admin.register(MasterData)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_id', 'module_name', 'module_description', 'created_at', 'modified_at')
    search_fields = ('module_name',)
    list_filter = ('created_at', 'modified_at')

@admin.register(MasterData)
class MasterDataAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'module', 'name_of_resource', 
        'type_of_resource', 'contact_details', 'pan', 
        'gst', 'address', 'work_location', 'work_type', 
        'experience', 'skill_set'
    )
    search_fields = ('name_of_resource__email', 'module__module_name')
    list_filter = ('type_of_resource', 'module', 'work_location')
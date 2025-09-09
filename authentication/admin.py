from django.contrib import admin
from .models import User

admin.site.register(User)
class userAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin', 'is_staff', 'is_active', 'id')
    search_fields = ('email', 'username')
    

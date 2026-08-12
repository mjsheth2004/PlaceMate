from django.contrib import admin
from .models import OfficerProfile

@admin.register(OfficerProfile)
class OfficerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_email', 'designation')
    search_fields = ('full_name', 'user__email', 'designation')

    @admin.display(ordering='user__email', description='User Email')
    def user_email(self, obj):
        return obj.user.email


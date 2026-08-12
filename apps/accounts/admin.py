from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'role', 'email_verified', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('role', 'email_verified', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'email_verified')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    actions = ['verify_email', 'unverify_email', 'make_active', 'make_inactive']

    @admin.action(description="Mark selected users as Email Verified")
    def verify_email(self, request, queryset):
        updated = queryset.update(email_verified=True)
        self.message_user(request, f"Successfully verified email for {updated} user(s).")

    @admin.action(description="Mark selected users as Email Unverified")
    def unverify_email(self, request, queryset):
        updated = queryset.update(email_verified=False)
        self.message_user(request, f"Successfully unverified email for {updated} user(s).")

    @admin.action(description="Activate selected user accounts")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} user(s).")

    @admin.action(description="Deactivate selected user accounts")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} user(s).")

admin.site.register(User, CustomUserAdmin)


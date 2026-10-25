from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import CompanyProfile

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = (
        'company_name', 
        'user_email', 
        'industry', 
        'location', 
        'website_link', 
        'verified_badge', 
        'created_at'
    )
    list_filter = ('is_verified', 'industry', 'created_at')
    search_fields = ('company_name', 'user__email', 'industry', 'location', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    actions = ['verify_companies', 'unverify_companies']

    @admin.display(ordering='user__email', description='Account Email')
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description='Website')
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
        return "-"

    @admin.display(ordering='is_verified', description='Verification Status')
    def verified_badge(self, obj):
        if obj.is_verified:
            return mark_safe('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">Verified</span>')
        return mark_safe('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">Unverified</span>')

    @admin.action(description="Verify selected companies")
    def verify_companies(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"Successfully verified {updated} company profile(s).")

    @admin.action(description="Unverify selected companies")
    def unverify_companies(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"Successfully unverified {updated} company profile(s).")


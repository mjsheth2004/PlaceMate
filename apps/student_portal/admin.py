from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import StudentProfile, Application

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'roll_number', 
        'user_email', 
        'department', 
        'semester', 
        'cgpa', 
        'passing_year', 
        'active_backlogs', 
        'verified_badge', 
        'created_at'
    )
    list_filter = ('department', 'semester', 'passing_year', 'is_verified', 'created_at')
    search_fields = ('full_name', 'roll_number', 'user__email', 'university')
    filter_horizontal = ('skills',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    actions = ['verify_students', 'unverify_students']

    @admin.display(ordering='user__email', description='Email')
    def user_email(self, obj):
        return obj.user.email

    @admin.display(ordering='is_verified', description='Status')
    def verified_badge(self, obj):
        if obj.is_verified:
            return mark_safe('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">Verified</span>')
        return mark_safe('<span style="background-color: #ffc107; color: #212529; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">Pending</span>')

    @admin.action(description="Verify selected student profiles")
    def verify_students(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"Successfully verified {updated} student profile(s).")

    @admin.action(description="Unverify selected student profiles")
    def unverify_students(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"Successfully unverified {updated} student profile(s).")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'student', 
        'drive', 
        'company_name', 
        'colored_status', 
        'applied_at', 
        'updated_at'
    )
    list_filter = ('status', 'applied_at', 'drive__company')
    search_fields = ('student__full_name', 'student__roll_number', 'student__user__email', 'drive__title', 'drive__company__company_name')
    date_hierarchy = 'applied_at'
    ordering = ('-applied_at',)

    actions = [
        'mark_as_shortlisted', 
        'mark_as_interview_scheduled', 
        'mark_as_selected', 
        'mark_as_rejected'
    ]

    @admin.display(ordering='drive__company__company_name', description='Company')
    def company_name(self, obj):
        return obj.drive.company.company_name

    @admin.display(ordering='status', description='Application Status')
    def colored_status(self, obj):
        colors = {
            'applied': '#17a2b8',
            'shortlisted': '#6f42c1',
            'interview_scheduled': '#fd7e14',
            'selected': '#28a745',
            'rejected': '#dc3545',
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.action(description="Mark selected applications as Shortlisted")
    def mark_as_shortlisted(self, request, queryset):
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f"Successfully marked {updated} application(s) as Shortlisted.")

    @admin.action(description="Mark selected applications as Interview Scheduled")
    def mark_as_interview_scheduled(self, request, queryset):
        updated = queryset.update(status='interview_scheduled')
        self.message_user(request, f"Successfully marked {updated} application(s) as Interview Scheduled.")

    @admin.action(description="Mark selected applications as Selected")
    def mark_as_selected(self, request, queryset):
        updated = queryset.update(status='selected')
        self.message_user(request, f"Successfully marked {updated} application(s) as Selected.")

    @admin.action(description="Mark selected applications as Rejected")
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"Successfully marked {updated} application(s) as Rejected.")


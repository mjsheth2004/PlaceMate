from django.contrib import admin
from django.utils.html import format_html
from .models import Department, Skill, PlacementDrive

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(PlacementDrive)
class PlacementDriveAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'company', 
        'salary_package_lpa', 
        'location', 
        'min_cgpa', 
        'max_backlogs', 
        'eligible_passing_year', 
        'application_deadline', 
        'colored_status', 
        'created_at'
    )
    list_filter = ('status', 'eligible_passing_year', 'eligible_departments', 'created_at')
    search_fields = ('title', 'company__company_name', 'location', 'job_description')
    filter_horizontal = ('eligible_departments', 'required_skills')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    actions = ['mark_as_published', 'mark_as_draft', 'mark_as_closed']

    @admin.display(ordering='salary_package', description='Package (LPA)')
    def salary_package_lpa(self, obj):
        return f"₹{obj.salary_package} LPA"

    @admin.display(ordering='status', description='Status')
    def colored_status(self, obj):
        colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'closed': '#dc3545',
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.action(description="Mark selected drives as Published")
    def mark_as_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f"Successfully published {updated} drive(s).")

    @admin.action(description="Mark selected drives as Draft")
    def mark_as_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f"Successfully set {updated} drive(s) to Draft.")

    @admin.action(description="Mark selected drives as Closed")
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f"Successfully closed {updated} drive(s).")


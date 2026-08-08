from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Application

@receiver(pre_save, sender=Application)
def track_previous_status(sender, instance, **kwargs):
    """Store previous status on instance to detect status changes in post_save."""
    if instance.pk:
        try:
            old_instance = Application.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Application.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Application)
def send_application_status_update_email(sender, instance, created, **kwargs):
    """Send email notification to student when application status is updated."""
    old_status = getattr(instance, '_old_status', None)
    current_status = instance.status

    # Send email only if status has changed (or on initial non-'applied' status)
    if old_status != current_status and current_status in ['shortlisted', 'interview_scheduled', 'selected', 'rejected']:
        student_user = instance.student.user
        drive = instance.drive
        
        status_labels = {
            'shortlisted': 'Shortlisted',
            'interview_scheduled': 'Interview Scheduled',
            'selected': 'Selected (Offer Extended)',
            'rejected': 'Update on Application'
        }
        
        status_display = status_labels.get(current_status, current_status.title())
        
        subject = f"Application Status Update: {drive.company.company_name} - {drive.title} [{status_display}]"
        
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        portal_url = f"{site_url}/student/applications/"
        
        html_message = render_to_string('emails/application_status_update.html', {
            'student_name': instance.student.full_name or student_user.username,
            'company_name': drive.company.company_name,
            'drive_title': drive.title,
            'status_display': status_display,
            'status_class': 'interview' if current_status == 'interview_scheduled' else current_status,
            'portal_url': portal_url
        })
        
        plain_message = f"""Hi {instance.student.full_name or student_user.username},

Your application status for {drive.title} at {drive.company.company_name} has been updated to: {status_display}.

Log in to PlaceMate to view more details: {portal_url}

Best regards,
PlaceMate Campus Placement Team
"""
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student_user.email],
                html_message=html_message,
                fail_silently=True
            )
        except Exception as e:
            print(f"Failed to send status update email: {e}")

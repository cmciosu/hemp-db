from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group

# Django Emails: https://docs.djangoproject.com/en/5.1/topics/email/

def email_admins(action: str, company_name: str, pending_change_id: int) -> None:
    """
    Sends an email notification to Admins and SrAdmins when a company has been created, edited, or deleted.

    Note that if the company name is a part of the edit, the new name will appear in the email.
    
    Parameters:
    action (str): Can only be 'created', 'edited', or 'deleted' depending on the action.
    company_name (str): Name of the company
    pending_change_id (int): ID of the pending change
    """

    # Invalid action
    if action not in ['created', 'edited', 'deleted']:
        return

    subject = f'[HempDB] Company {action} (Pending Review)'
    
    # Plaintext
    text_message = f"""
    A company called "{company_name}" has been {action} and is now pending review.
    
    View this pending change at: {settings.SITE_URL}/companies_pending/{pending_change_id}
    View all pending changes at: {settings.SITE_URL}/changes
    """

    # HTML (clickable links)
    html_message = f"""
    <p>A company called "{company_name}" has been {action} and is now pending review.</p>
    
    <p>View this pending change <a href="{settings.SITE_URL}/companies_pending/{pending_change_id}">here</a>.</p>
    <p>View all pending changes <a href="{settings.SITE_URL}/changes">here</a>.</p>
    """

    # Group IDs from auth_group containing 'admin' (case insensitive)
    admin_groups = Group.objects.filter(name__icontains='admin')
    admin_group_ids = admin_groups.values_list('id', flat=True)

    # Get list of emails for all users that are some form of admin
    admin_emails = list(User.objects.filter(groups__id__in=admin_group_ids).values_list('email', flat=True).distinct())

    send_mail(
        subject=subject,
        message=text_message,
        from_email=None,    # Uses DEFAULT_FROM_EMAIL
        html_message=html_message,
        recipient_list=admin_emails,
        fail_silently=True
    )

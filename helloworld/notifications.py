from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group

# Django Emails: https://docs.djangoproject.com/en/5.1/topics/email/
"""
Todo (In-Progress)
- Create method to notify of a pending company edit, not pending new company
- Create method for when # of pending changes meets a threshold
"""
def notify_admins_pending_new_company(company_name: str, pending_change_id: int) -> None:
    """
    Sends email notification to Admins and SrAdmins when a new company is created (pending)
    
    Parameters:
    company_name (str): Name of the pending company
    pending_change_id (int): ID of the pending company
    """

    subject = '[HempDB] New Pending Company'
    
    # Plaintext
    text_message = f"""
    A new company called "{company_name}" has been created and is now pending.
    
    View this pending change at: {settings.SITE_URL}/companies_pending/{pending_change_id}
    View all pending changes at: {settings.SITE_URL}/changes
    """

    # HTML (clickable links)
    html_message = f"""
    <p>A new company called "{company_name}" has been created and is now pending.</p>
    
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

import logging
import os
from pathlib import Path
from datetime import datetime
from django_cron import CronJobBase, Schedule, logging
from helloworld.management.commands.audit import Command as Audit
from django.core.mail import EmailMessage
from django.contrib.auth.models import User, Group

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
AUDITLOGS_PATH = BASE_DIR / 'management' / 'commands' / 'auditlogs'


def get_audit_file():
    assert(BASE_DIR.exists())
    assert(AUDITLOGS_PATH.exists())

    csv_files = list(file for file in AUDITLOGS_PATH.iterdir())

    if not csv_files: # no csv files in the auditlogs
        return None, None

    latest_file = max(csv_files, key=lambda f: f.stat().st_mtime) # pulling metadata from audit log files for time created
    modified_time = datetime.fromtimestamp(latest_file.stat().st_mtime)

    return latest_file.name, modified_time.date()



class CronAudit(CronJobBase):
    RUN_EVERY_MINS = 30240 # 30240 = 3 weeks worth of minutes (NOT CURRENTLY IN USE)
    # Schedule is necessary for the cron job to be properly recognized
    # Future development would involve using some third party service to trigger this on a regular basis,
    #    but currently it is serving as a placeholder to fill a requirement of Django's basic cron job recognition
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'helloworld.CronAudit'

    def do(self):
        
        logger.info("Cron Audit Job Starting...")
        # Group IDs from admin authority group
        admin_groups = Group.objects.filter(name='Admin')
        admin_group_ids = admin_groups.values_list('id', flat=True)
            # Get list of emails for all users that are some form of admin
        admin_emails = list(User.objects.filter(groups__id__in=admin_group_ids).values_list('email', flat=True).distinct())

        # Pull default sender email address from .env file
        EMAIL_USER = os.getenv("EMAIL_USER")
        
        # Make sure personal email is specified in personal .env file to receive emails from the audit generation on success or failure.
        AUDIT_RECIPIENT = os.getenv("AUDIT_RECIPIENT")

        try:
            audit = Audit()
            audit.handle()
            logger.info("Audit Complete")
            auditlog, filedate = get_audit_file()

            if not auditlog or not filedate:
                raise Exception("Invalid auditlog file found, please reference the directory you are trying to access to resolve this issue.")

            file_path = AUDITLOGS_PATH / auditlog

            ##
            ## Note: Specify list of people to receive the email report under 'to' parameter list
            ##
            with open(file_path, 'rb') as file:
                email = EmailMessage(
                    subject=f"[HempDB] Database Audit Log Generation {filedate}",
                    body=f"The Database Audit job was successful, the new file created is attached to this message with the name: {auditlog}. The file is available for developers under the directory: hemp-db/helloworld/management/commands/auditlogs.",
                    from_email=EMAIL_USER,
                    to=[AUDIT_RECIPIENT]
                )

                email.attach(auditlog, file.read(), 'text/csv')
                email.send()
            



        except Exception as e:
            logger.exception("Auditing failed", exc_info=True)
            email = EmailMessage(
                subject=f"[HempDB] Database Audit Log Failure {filedate}",
                body=f"The Database Audit job failed. Please alert developers to the status of the audit generation. The following error is:\n\n\n{e}",
                from_email=EMAIL_USER,
                to=[AUDIT_RECIPIENT]
            )
            email.send()

    def on_failure(self, exc):
        logger.exception(f"Audit Failed: {exc}")

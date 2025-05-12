import logging
from pathlib import Path
from datetime import datetime
from django_cron import CronJobBase, Schedule, logging
from django.core.mail import mail_admins
from helloworld.management.commands.audit import Command as Audit

logger = logging.getLogger(__name__)

def get_audit_file():
    path = Path('helloworld/management/auditlogs')
    csv_files = list(path.glob("*.csv"))

    if not csv_files: # no csv files in the auditlogs
        return None, None

    latest_file = max(csv_files, key=lambda f: f.stat().st_mtime) # pulling metadata from audit log files for time created
    modified_time = datetime.fromtimestamp(latest_file.stat().st_mtime)

    return latest_file.name, modified_time.date()



class CronAudit(CronJobBase):
    RUN_EVERY_MINS = 30240 # 30240 = 3 weeks worth of minutes
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'helloworld.CronAudit'

    def do(self):
        
        logger.info("Cron Audit Job Starting...")

        try:
            Audit.handle()
            logger.info("Audit Complete")
            auditlog, filedate = get_audit_file()
            
            # Specific administrators who should receive emails must be listed in settings.py under `ADMINS`
            mail_admins(f"Latest Audit File {auditlog} created on {filedate}") # Test this at a later date 

        except Exception as e:
            logger.exception("Auditing failed", exc_info=True)
            mail_admins("Audit Failed", str(e))

    def on_failure(self, exc):
        logger.exception(f"Audit Failed: {exc}")

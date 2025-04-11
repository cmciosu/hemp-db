import os
from pathlib import Path
from datetime import datetime
from django_cron import CronJobBase, Schedule, logging
from django.core.management import call_command
from helloworld.models import Company



def get_audit_file():
    path = Path('helloworld/management/auditlogs')
    csv_files = list(path.glob("*.csv"))

    if not csv_files: # no csv files in the auditlogs
        return None, None

    latest_file = max(csv_files, key=lambda f: f.stat().st_mtime) # pulling metadata from audit log files for time created
    modified_time = datetime.fromtimestamp(latest_file.stat().st_mtime)

    return latest_file.name, modified_time.date()



class CronAudit(logging.CronJobBase):
    execution_interval = 30240 # 3 weeks worth of minutes

    schedule = Schedule(run_every_mins=execution_interval)
    code = 'helloworld.CronAudit'

    def do(self):
        
        print("Cron Job Starting...")

        call_command('audit') # execute audit

        print("Cron Job Complete")

        auditlog, filedate = get_audit_file()
        print(f"Latest Audit File {auditlog} modified on {filedate}")


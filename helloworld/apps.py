from django.apps import AppConfig
from django.db.models.signals import m2m_changed

class HelloworldConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "helloworld"

    # Runs on startup
    def ready(self):
        import helloworld.signals   # Connect the signal handlers defined in signals.py
        m2m_changed.connect(helloworld.signals.update_is_staff_on_group_change) # Explicitly connect (Satisfies ruff check)
from django.apps import AppConfig


class HelloworldConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "helloworld"

    # Runs on startup
    def ready(self):
        import helloworld.signals   # Loads the signals defined in signals.py

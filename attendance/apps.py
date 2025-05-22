from django.apps import AppConfig
import os


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'

    def ready(self):
        super().ready()
        if os.environ.get("RUN_MAIN") == "true":  # Only start in main process
            try:
                from .scheduler import start
                print('Starting APScheduler...')
                start()
            except Exception as e:
                import traceback
                print('Scheduler failed to start:', e)
                traceback.print_exc()

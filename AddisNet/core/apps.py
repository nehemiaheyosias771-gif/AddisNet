from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'AddisNet Core - Smart City Management'
    
    def ready(self):
        # Import signal handlers
        try:
            from . import signals
        except ImportError:
            pass

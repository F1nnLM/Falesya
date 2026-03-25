from django.apps import AppConfig

class UtentiConfig(AppConfig):
    name = 'apps.utenti'

    def ready(self):
        import apps.utenti.models  
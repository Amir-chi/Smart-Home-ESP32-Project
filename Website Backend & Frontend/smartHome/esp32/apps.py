from django.apps import AppConfig


class Esp32Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'esp32'


    def ready(self):
        import esp32.signals
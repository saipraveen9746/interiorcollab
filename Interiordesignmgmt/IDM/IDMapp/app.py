from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'IDMapp'

    def ready(self):
        import IDMapp.signals  # import signals module
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.polls'

    # 定時処理
    def ready(self):
        from .schedule import start
        start()
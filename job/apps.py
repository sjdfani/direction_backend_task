from django.apps import AppConfig


class JobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job'

    def ready(self) -> None:
        from .tasks import main
        main()

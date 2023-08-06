from django.apps import AppConfig


class DjangoEveonlineTimerboardConfig(AppConfig):
    name = 'django_eveonline_timerboard'
    verbose_name = 'EVE Online Timers'
    url_slug = 'eveonline'

    def ready(self):
        from .bindings import create_bindings
        create_bindings()
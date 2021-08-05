from django.apps import AppConfig


class BtcConfig(AppConfig):
    name = 'btc'

    def ready(self):
        import btc.signals

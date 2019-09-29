from django.apps import AppConfig

class DjangoAdmobSSVConfig(AppConfig):
	name = 'django_admob_ssv'

    def ready(self):
        import django_admob_ssv.signals

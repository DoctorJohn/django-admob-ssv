from django.apps import AppConfig


class VerificationsConfig(AppConfig):
    name = "tests.project.verifications"

    def ready(self):
        import tests.project.verifications.signals  # noqa: F401

from django.apps import AppConfig


class RewardsConfig(AppConfig):
    name = "tests.project.rewards"

    def ready(self):
        import tests.project.rewards.signals  # noqa: F401

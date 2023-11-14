from datetime import timedelta

from django.conf import settings as django_settings


class Settings:
    @property
    def keys_server_url(self) -> str:
        return getattr(
            django_settings,
            "ADMOB_SSV_KEYS_SERVER_URL",
            "https://www.gstatic.com/admob/reward/verifier-keys.json",
        )

    @property
    def keys_cache_timeout(self) -> timedelta:
        return getattr(
            django_settings,
            "ADMOB_SSV_KEYS_CACHE_TIMEOUT",
            timedelta(days=1),
        )

    @property
    def keys_cache_key(self) -> str:
        return getattr(
            django_settings,
            "ADMOB_SSV_KEYS_CACHE_KEY",
            "admob_ssv.public_keys",
        )


settings = Settings()

from django.conf import settings
from datetime import timedelta


ADMOB_SSV_KEYS_SERVER_URL = getattr(
    settings,
    "ADMOB_SSV_KEYS_SERVER_URL",
    "https://www.gstatic.com/admob/reward/verifier-keys.json",
)

ADMOB_SSV_KEYS_CACHE_TIMEOUT = getattr(
    settings,
    "ADMOB_SSV_KEYS_CACHE_TIMEOUT",
    timedelta(days=1),
)

ADMOB_SSV_KEYS_CACHE_KEY = getattr(
    settings,
    "ADMOB_SSV_KEYS_CACHE_KEY",
    "admob_ssv.public_keys",
)

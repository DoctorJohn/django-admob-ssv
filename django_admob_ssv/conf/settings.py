from django.conf import settings


ADMOB_SSV_KEY_SERVER_URL = getattr(
    settings,
    'ADMOB_SSV_KEY_SERVER_URL',
    'https://www.gstatic.com/admob/reward/verifier-keys.json',
)

ADMOB_SSV_KEYS_CACHE_TIMEOUT = getattr(
    settings,
    'ADMOB_SSV_KEYS_CACHE_TIMEOUT',
    24 * 60 * 60,  # 24 hours in seconds
)

ADMOB_SSV_KEYS_CACHE_KEY = getattr(
    settings,
    'ADMOB_SSB_KEYS_CACHE_KEY',
    'django_admob_ssv.public_keys',
)

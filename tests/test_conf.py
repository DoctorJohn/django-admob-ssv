from datetime import timedelta

from admob_ssv.conf import settings as admob_ssv_settings


def test_settings_keys_server_url_default(settings):
    del settings.ADMOB_SSV_KEYS_SERVER_URL
    assert (
        admob_ssv_settings.keys_server_url
        == "https://www.gstatic.com/admob/reward/verifier-keys.json"
    )


def test_settings_keys_server_url_override(settings):
    settings.ADMOB_SSV_KEYS_SERVER_URL = "https://example.com/keys.json"
    assert admob_ssv_settings.keys_server_url == "https://example.com/keys.json"


def test_settings_keys_cache_timeout_default(settings):
    del settings.ADMOB_SSV_KEYS_CACHE_TIMEOUT
    assert admob_ssv_settings.keys_cache_timeout == timedelta(days=1)


def test_settings_keys_cache_timeout_override(settings):
    settings.ADMOB_SSV_KEYS_CACHE_TIMEOUT = timedelta(days=2)
    assert admob_ssv_settings.keys_cache_timeout == timedelta(days=2)


def test_settings_keys_cache_key_default(settings):
    del settings.ADMOB_SSV_KEYS_CACHE_KEY
    assert admob_ssv_settings.keys_cache_key == "admob_ssv.public_keys"


def test_settings_keys_cache_key_override(settings):
    settings.ADMOB_SSV_KEYS_CACHE_KEY = "custom_cache_key"
    assert admob_ssv_settings.keys_cache_key == "custom_cache_key"

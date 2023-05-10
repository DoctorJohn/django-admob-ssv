# Django Admob server-side verification (SSV)

[![PyPI][pypi-image]][pypi-url]
![PyPI - Python Version][python-image]
![PyPI - Django Version][django-image]
[![License][license-image]][license-url]
[![Tests][tests-image]][tests-url]

[pypi-image]: https://img.shields.io/pypi/v/django-admob-ssv
[pypi-url]: https://pypi.org/project/django-admob-ssv/
[python-image]: https://img.shields.io/pypi/pyversions/django-admob-ssv
[django-image]: https://img.shields.io/pypi/djversions/django-admob-ssv
[license-image]: https://img.shields.io/pypi/l/django-admob-ssv
[license-url]: https://github.com/DoctorJohn/django-admob-ssv/blob/master/LICENSE
[tests-image]: https://github.com/DoctorJohn/django-admob-ssv/workflows/Tests/badge.svg
[tests-url]: https://github.com/DoctorJohn/django-admob-ssv/actions

A Django app providing a view for handling Admob server-side verification callbacks.
Successfully verified callbacks trigger a custom Django signal.
Apps in your project may listen to that signal and reward the user
based on the information received via the callback.

Taken from the [Admob SSV documentation](https://developers.google.com/admob/android/rewarded-video-ssv):

> Server-side verification callbacks are URL requests, with query parameters expanded by Google, that are sent by Google to an external system to notify it that a user should be rewarded for interacting with a rewarded video ad. Rewarded video SSV (server-side verification) callbacks provide an extra layer of protection against spoofing of client-side callbacks to reward users.

## Installation

```sh
pip install django-admob-ssv
```

## Configuration

1. Add a `path` for the `admob_ssv.views.AdmobSSVView` view to your `urlpatterns`.

```python
from django.urls import path
from admob_ssv.views import AdmobSSVView


urlpatterns = [
    path('admob-ssv/', AdmobSSVView.as_view()),
]
```

2. Listen to the `admob_ssv.signals.valid_admob_ssv` signal.

```python
from django.dispatch import receiver
from admob_ssv.signals import valid_admob_ssv


@receiver(valid_admob_ssv)
def reward_user(sender, query, **kwargs):
    ad_network = query.get('ad_network')
    ad_unit = query.get('ad_unit')
    custom_data = query.get('custom_data')
    # ...
```

Take a look at this [list of all SSV callback parameters](https://developers.google.com/admob/android/rewarded-video-ssv).

Also make sure you [connect your receiver properly](https://docs.djangoproject.com/en/4.2/topics/signals/#connecting-receiver-functions), otherwise it won't get called. (Take a look at the "Where should this code live?" box).

## Advanced configuration

You may optionally set the following options in your Django `settings.py` file.
The code snippet below shows the default values used.

```python
from datetime import timedelta


ADMOB_SSV_KEY_SERVER_URL = "https://www.gstatic.com/admob/reward/verifier-keys.json",

ADMOB_SSV_KEYS_CACHE_TIMEOUT = timedelta(days=1)

ADMOB_SSV_KEYS_CACHE_KEY = "admob_ssv.public_keys"
```

## Example project

Take a look at our Django example project under `tests/project`.
You can run it by executing these commands:

1. `poetry install`
2. `poetry run python tests/project/manage.py migrate`
3. `poetry run python tests/project/manage.py createsuperuser`
4. `poetry run python tests/project/manage.py runserver`

# Django Admob Server-Side Verification (SSV)

![PyPI](https://img.shields.io/pypi/v/django-admob-ssv)
![PyPI - License](https://img.shields.io/pypi/l/django-admob-ssv)

A Django app providing a view that handles Admob Server-Side Verification callbacks. Successfull verifications trigger a custom signal. Separate apps may listen to that signal and reward the user based on the information received via the callback.

Taken from the [Admob SSV documentation](https://developers.google.com/admob/android/rewarded-video-ssv):

Server-side verification callbacks are URL requests, with query parameters expanded by Google, that are sent by Google to an external system to notify it that a user should be rewarded for interacting with a rewarded video ad. Rewarded video SSV (server-side verification) callbacks provide an extra layer of protection against spoofing of client-side callbacks to reward users.

## Requirements

- Python 3
- [Django](https://pypi.org/project/Django/) (version 1.11+)
- [ecdsa](https://pypi.org/project/ecdsa/)

## Installation

```pip install django-admob-ssv```

## Configuration

1. Add a ```path``` for the ```admob_ssv.views.admob_ssv``` view to your ```urlpatterns```.

```python
from django.urls import path
from admob_ssv.views import admob_ssv

urlpatterns = [
    path('admob-ssv/', admob_ssv),
]
```

2. Listen to the ```admob_ssv.signals.valid_admob_ssv``` signal.

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

Also make sure you [connect your receiver properly](https://docs.djangoproject.com/en/2.2/topics/signals/#connecting-receiver-functions), otherwise it won't get called. (Take a look at the "Where should this code live?" box).

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

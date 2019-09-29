from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.core.cache import cache
from django_admob_ssv.conf import settings
from django_admob_ssv.signals import valid_admob_ssv
from django_admob_ssv.utils import fetch_public_keys, verify_signature


SIGNATURE_PARAM_NAME = 'signature'
KEY_ID_PARAM_NAME = 'key_id'
REQUIRED_PARAM_NAMES = (SIGNATURE_PARAM_NAME, KEY_ID_PARAM_NAME)


@require_GET
def admob_ssv(request):
    for query_param_name in REQUIRED_PARAM_NAMES:
        if query_param_name not in request.GET:
            return HttpResponseBadRequest()
    
    # The last two query parameters of rewarded video SSV callbacks are always
    # signature and key_id, in that order. The remaining query parameters specify
    # the content to be verified. 
    key_id = request.GET[KEY_ID_PARAM_NAME]
    signature = request.GET[SIGNATURE_PARAM_NAME]
    content = request.META['QUERY_STRING']
    content = content[:content.index('&' + SIGNATURE_PARAM_NAME)]
    
    admob_public_keys = cache.get_or_set(
        settings.ADMOB_SSV_KEYS_CACHE_KEY,
        fetch_public_keys(),
        settings.ADMOB_SSV_KEYS_CACHE_TIMEOUT
    )

    public_key = admob_public_keys.get(key_id, None)
    if public_key is None:
        return HttpResponseBadRequest()

    if verify_signature(public_key['pem'], content, signature):
        valid_admob_ssv.send(sender=None, query=request.GET.dict())
        return HttpResponse()
    return HttpResponseBadRequest()

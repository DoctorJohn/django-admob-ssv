import math
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.core.cache import cache
from admob_ssv.conf import settings
from admob_ssv.signals import valid_admob_ssv
from ecdsa import VerifyingKey, BadSignatureError
from ecdsa.util import sigdecode_der
import hashlib
import base64
import urllib
import json


class AdmobSSVView(View):
    SIGNATURE_PARAM_NAME = "signature"
    KEY_ID_PARAM_NAME = "key_id"
    REQUIRED_PARAM_NAMES = (SIGNATURE_PARAM_NAME, KEY_ID_PARAM_NAME)

    def get(self, request, *args, **kwargs):
        for query_param_name in self.REQUIRED_PARAM_NAMES:
            if query_param_name not in request.GET:
                return HttpResponseBadRequest()

        # The last two query parameters of rewarded video SSV callbacks are always
        # signature and key_id, in that order. The remaining query parameters specify
        # the content to be verified.
        key_id = request.GET[self.KEY_ID_PARAM_NAME]
        signature = request.GET[self.SIGNATURE_PARAM_NAME]
        content = request.META["QUERY_STRING"]
        content = content[: content.index("&" + self.SIGNATURE_PARAM_NAME)]

        admob_public_keys = cache.get_or_set(
            settings.ADMOB_SSV_KEYS_CACHE_KEY,
            self.fetch_public_keys(),
            math.floor(settings.ADMOB_SSV_KEYS_CACHE_TIMEOUT.total_seconds()),
        )

        public_key = admob_public_keys.get(key_id, None)
        if public_key is None:
            return HttpResponseBadRequest()

        if self.verify_signature(public_key["pem"], content, signature):
            valid_admob_ssv.send(sender=None, query=request.GET.dict())
            return HttpResponse()
        return HttpResponseBadRequest()

    def fetch_public_keys():
        keys = dict()
        url = settings.ADMOB_SSV_KEYS_SERVER_URL

        try:
            with urllib.request.urlopen(url) as response:
                if response.getcode() != 200:
                    return keys
                data = response.read().decode()
        except urllib.URLError:
            return keys

        json_data = json.loads(data)

        for key in json_data["keys"]:
            keys[str(key["keyId"])] = {
                "pem": key["pem"],
                "base64": key["base64"],
            }
        return keys

    def verify_signature(pem, msg, sig):
        prepared_key = VerifyingKey.from_pem(pem)
        prepared_msg = (urllib.parse.unquote(msg)).encode("utf-8")

        # Ensure that the signatures padding is always a multiple of 4. Note that
        # the decode function will ignore extraneous padding. Before the decode
        # method would occasionaly yield the following exception:
        # binascii.Error: Incorrect padding
        prepared_sig = base64.urlsafe_b64decode(sig + "===")

        try:
            return prepared_key.verify(
                prepared_sig,
                prepared_msg,
                hashfunc=hashlib.sha256,
                sigdecode=sigdecode_der,
            )
        except BadSignatureError:
            return False

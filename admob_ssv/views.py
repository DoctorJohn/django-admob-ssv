import hashlib
import base64
import urllib
import math
import requests
from typing import Dict, Optional
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.views import View
from django.core.cache import cache
from admob_ssv.conf import settings
from admob_ssv.signals import valid_admob_ssv


class AdmobSSVView(View):
    SIGNATURE_PARAM_NAME = "signature"
    KEY_ID_PARAM_NAME = "key_id"
    REQUIRED_PARAM_NAMES = (SIGNATURE_PARAM_NAME, KEY_ID_PARAM_NAME)

    def get(self, request: HttpRequest) -> HttpResponse:
        for param_name in self.REQUIRED_PARAM_NAMES:
            if param_name not in request.GET:
                return HttpResponseBadRequest()

        key_id = request.GET[self.KEY_ID_PARAM_NAME]
        public_key = self.get_public_key(key_id)

        if public_key is None:
            return HttpResponseBadRequest()

        signature = self.get_signature(request)
        content = self.get_unverified_content(request)

        if self.verify_signature(public_key, signature, content):
            valid_admob_ssv.send(sender=None, query=request.GET.dict())
            return HttpResponse()

        return HttpResponseBadRequest()

    def get_signature(self, request: HttpRequest) -> str:
        encoded_signature = request.GET[self.SIGNATURE_PARAM_NAME]

        # Ensure that the signatures padding is always a multiple of 4. Note that
        # the decode function will ignore extraneous padding. Before the decode
        # method would occasionaly yield the following exception:
        # binascii.Error: Incorrect padding
        return base64.urlsafe_b64decode(encoded_signature + "===")

    def get_unverified_content(self, request: HttpRequest) -> str:
        # According to the Admob SSV documentation, the last two query
        # parameters of rewarded video SSV callbacks are always
        # signature and key_id, in that order. The remaining query
        # parameters specify the content to be verified.
        query_string = request.META["QUERY_STRING"]
        signature_start_index = query_string.index(f"&{self.SIGNATURE_PARAM_NAME}=")
        encoded_content = query_string[:signature_start_index]
        return urllib.parse.unquote(encoded_content)

    def get_public_key(self, key_id: str) -> Optional[str]:
        cached_public_keys = cache.get(settings.ADMOB_SSV_KEYS_CACHE_KEY, default={})
        cached_public_key = cached_public_keys.get(key_id, None)

        if cached_public_key is not None:
            return cached_public_key

        fetched_public_keys = self.fetch_public_keys()
        cache.set(
            settings.ADMOB_SSV_KEYS_CACHE_KEY,
            fetched_public_keys,
            math.floor(settings.ADMOB_SSV_KEYS_CACHE_TIMEOUT.total_seconds()),
        )
        return fetched_public_keys.get(key_id, None)

    def fetch_public_keys(self) -> Dict[str, str]:
        response = requests.get(settings.ADMOB_SSV_KEYS_SERVER_URL)
        response.raise_for_status()
        json_data = response.json()
        return {str(key["keyId"]): key["pem"] for key in json_data["keys"]}

    def verify_signature(self, public_key: str, signature: str, content: str) -> bool:
        from ecdsa import VerifyingKey, BadSignatureError
        from ecdsa.util import sigdecode_der

        verifying_key = VerifyingKey.from_pem(public_key)

        try:
            return verifying_key.verify(
                signature,
                content,
                hashfunc=hashlib.sha256,
                sigdecode=sigdecode_der,
            )
        except BadSignatureError:
            return False

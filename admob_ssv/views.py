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

    def get(self, request: HttpRequest) -> HttpResponse:
        if self.SIGNATURE_PARAM_NAME not in request.GET:
            return HttpResponseBadRequest("Missing signature")

        if self.KEY_ID_PARAM_NAME not in request.GET:
            return HttpResponseBadRequest("Missing key_id")

        key_id = request.GET[self.KEY_ID_PARAM_NAME]
        public_key = self.get_public_key(key_id)

        if public_key is None:
            return HttpResponseBadRequest("Unknown key_id")

        signature = self.get_signature(request)
        content = self.get_unverified_content(request)

        if self.verify_signature(public_key, signature, content):
            self.handle_valid_ssv(request)
            return HttpResponse()

        return HttpResponseBadRequest("Invalid signature")

    def get_signature(self, request: HttpRequest) -> bytes:
        encoded_signature = request.GET[self.SIGNATURE_PARAM_NAME]

        # Ensure that the signatures padding is always a multiple of 4. Note that
        # the decode function will ignore extraneous padding. Before the decode
        # method would occasionaly yield the following exception:
        # binascii.Error: Incorrect padding
        return base64.urlsafe_b64decode(encoded_signature + "===")

    def get_unverified_content(self, request: HttpRequest) -> bytes:
        # According to the Admob SSV documentation, the last two query
        # parameters of rewarded video SSV callbacks are always
        # signature and key_id, in that order. The remaining query
        # parameters specify the content to be verified.
        query_string = request.META["QUERY_STRING"]
        signature_start_index = query_string.index(f"&{self.SIGNATURE_PARAM_NAME}=")
        escaped_content = query_string[:signature_start_index]
        return urllib.parse.unquote(escaped_content).encode("utf-8")

    def get_public_key(self, key_id: str) -> Optional[str]:
        cached_public_keys = cache.get(settings.keys_cache_key, default={})
        cached_public_key = cached_public_keys.get(key_id, None)

        if cached_public_key is not None:
            return cached_public_key

        fetched_public_keys = self.fetch_public_keys()
        cache.set(
            settings.keys_cache_key,
            fetched_public_keys,
            math.floor(settings.keys_cache_timeout.total_seconds()),
        )
        return fetched_public_keys.get(key_id, None)

    def fetch_public_keys(self) -> Dict[str, str]:
        response = requests.get(settings.keys_server_url)
        response.raise_for_status()
        json_data = response.json()
        return {str(key["keyId"]): key["pem"] for key in json_data["keys"]}

    def verify_signature(
        self, public_key: str, signature: bytes, content: bytes
    ) -> bool:
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

    def handle_valid_ssv(self, request: HttpRequest) -> None:
        valid_admob_ssv.send(sender=None, query=request.GET.dict())

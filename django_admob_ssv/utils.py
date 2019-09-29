from django_admob_ssv.conf import settings
from ecdsa import VerifyingKey, BadSignatureError
from ecdsa.util import sigdecode_der
import hashlib
import base64
import urllib
import json


def fetch_public_keys():
    keys = dict()
    url = settings.ADMOB_SSV_KEY_SERVER_URL

    try:
        with urllib.request.urlopen(url) as response:
            if response.getcode() != 200:
                return keys
            data = response.read().decode()
    except urllib.URLError as e:
        return keys

    json_data = json.loads(data)

    for key in json_data['keys']:
        keys[str(key['keyId'])] = {
            'pem': key['pem'],
            'base64': key['base64'],
        }
    return keys


def verify_signature(pem, msg, sig):
    prepared_key = VerifyingKey.from_pem(pem)
    prepared_msg = (urllib.parse.unquote(msg)).encode('utf-8')
    prepared_sig = base64.urlsafe_b64decode(sig)

    try:
        return prepared_key.verify(
            prepared_sig,
            prepared_msg,
            hashfunc=hashlib.sha256,
            sigdecode=sigdecode_der,
        )
    except BadSignatureError as e:
        return False

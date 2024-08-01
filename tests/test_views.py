import base64
import binascii
import random
from unittest import mock

import pytest
from django.core.cache import cache

from admob_ssv.views import AdmobSSVView
from tests.project.verifications.models import Verification

PUBLIC_KEY_PEM = """
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+nzvoGqvDeB9+SzE6igTl7TyK4JB
bglwir9oTcQta8NuG26ZpZFxt+F2NDk7asTE6/2Yc8i1ATcGIqtuS5hv0Q==
-----END PUBLIC KEY-----
"""


@pytest.fixture(autouse=True)
def mock_admob_ssv_keys_server(requests_mock):
    requests_mock.get(
        "https://www.gstatic.com/admob/reward/verifier-keys.json",
        json={
            "keys": [
                {
                    "keyId": 3335741209,
                    "pem": PUBLIC_KEY_PEM,
                    "base64": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+nzvoGqvDeB9+SzE6igTl7TyK4JBbglwir9oTcQta8NuG26ZpZFxt+F2NDk7asTE6/2Yc8i1ATcGIqtuS5hv0Q==",
                }
            ]
        },
    )


@pytest.mark.django_db
def test_get_with_valid_callback(client):
    response = client.get(
        path="/admob-ssv/",
        data={
            "ad_network": 5450213213286189855,
            "ad_unit": 1234567890,
            "custom_data": "customdata42",
            "reward_amount": 1,
            "reward_item": "Reward",
            "timestamp": 1683852940453,
            "transaction_id": 123456789,
            "user_id": "userid42",
            "signature": "MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q",
            "key_id": 3335741209,
        },
    )

    assert response.status_code == 200
    assert Verification.objects.filter(
        ad_network=5450213213286189855,
        ad_unit=1234567890,
        custom_data="customdata42",
        key_id=3335741209,
        reward_amount=1,
        reward_item="Reward",
        signature="MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q",
        timestamp=1683852940453,
        transaction_id="123456789",
        user_id="userid42",
    ).exists()


@pytest.mark.django_db
def test_get_with_base64_encoded_payload(client):
    response = client.get(
        path="/admob-ssv/",
        data={
            "ad_network": 5450213213286189855,
            "ad_unit": 1234567890,
            "custom_data": "8b626840-a5bb-4732-a02b-67517d6b9443",
            "reward_amount": 1,
            "reward_item": "Boost",
            "timestamp": 1683939248995,
            "transaction_id": 123456789,
            "user_id": "VXNlcjo0Mg==",
            "signature": "MEQCIGdfQR4eu9bOi3gg069p0ZcH5H-u3etEFQsSJZ4fPU_EAiB75fI8p8uKetMld8_wT3GNPuGnnJYNpHN2ZP9u7bcpiA",
            "key_id": 3335741209,
        },
    )

    assert response.status_code == 200
    assert Verification.objects.filter(
        ad_network=5450213213286189855,
        ad_unit=1234567890,
        custom_data="8b626840-a5bb-4732-a02b-67517d6b9443",
        key_id=3335741209,
        reward_amount=1,
        reward_item="Boost",
        signature="MEQCIGdfQR4eu9bOi3gg069p0ZcH5H-u3etEFQsSJZ4fPU_EAiB75fI8p8uKetMld8_wT3GNPuGnnJYNpHN2ZP9u7bcpiA",
        timestamp=1683939248995,
        transaction_id="123456789",
        user_id="VXNlcjo0Mg==",
    ).exists()


@pytest.mark.django_db
def test_get_with_valid_callback_and_unordered_query_parameters(client):
    params = [
        ("ad_network", 5450213213286189855),
        ("ad_unit", 1234567890),
        ("custom_data", "customdata42"),
        ("key_id", 3335741209),
        ("reward_amount", 1),
        ("reward_item", "Reward"),
        (
            "signature",
            "MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q",
        ),
        ("timestamp", 1683852940453),
        ("transaction_id", 123456789),
        ("user_id", "userid42"),
    ]

    random.shuffle(params)

    response = client.get(
        path="/admob-ssv/",
        data=dict(params),
    )

    assert response.status_code == 200
    assert Verification.objects.filter(
        ad_network=5450213213286189855,
        ad_unit=1234567890,
        custom_data="customdata42",
        key_id=3335741209,
        reward_amount=1,
        reward_item="Reward",
        signature="MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q",
        timestamp=1683852940453,
        transaction_id="123456789",
        user_id="userid42",
    ).exists()


def test_get_with_missing_signature(client):
    response = client.get(
        path="/admob-ssv/",
        data={
            "ad_network": 5450213213286189855,
            "ad_unit": 1234567890,
            "custom_data": "customdata42",
            "reward_amount": 1,
            "reward_item": "Reward",
            "timestamp": 1683852940453,
            "transaction_id": 123456789,
            "user_id": "userid42",
            "key_id": 3335741209,
        },
    )

    assert response.status_code == 400
    assert response.content == b"Missing signature"


def test_get_with_missing_key_id(client):
    response = client.get(
        path="/admob-ssv/",
        data={
            "ad_network": 5450213213286189855,
            "ad_unit": 1234567890,
            "custom_data": "customdata42",
            "reward_amount": 1,
            "reward_item": "Reward",
            "timestamp": 1683852940453,
            "transaction_id": 123456789,
            "user_id": "userid42",
            "signature": "MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q",
        },
    )

    assert response.status_code == 400
    assert response.content == b"Missing key_id"


def test_get_with_unknown_key_id(client):
    response = client.get(
        path="/admob-ssv/",
        data={
            "ad_network": 5450213213286189855,
            "ad_unit": 1234567890,
            "custom_data": "customdata42",
            "reward_amount": 1,
            "reward_item": "Reward",
            "timestamp": 1683852940453,
            "transaction_id": 123456789,
            "user_id": "userid42",
            "signature": "MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q",
            "key_id": "unknown",
        },
    )

    assert response.status_code == 400
    assert response.content == b"Unknown key_id"


def test_get_with_invalid_signature(client):
    response = client.get(
        path="/admob-ssv/",
        data={
            "ad_network": 5450213213286189855,
            "ad_unit": 1234567890,
            "custom_data": "TEMPERED CUSTOM DATA",
            "reward_amount": 1,
            "reward_item": "Reward",
            "timestamp": 1683852940453,
            "transaction_id": 123456789,
            "user_id": "userid42",
            "signature": "MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q",
            "key_id": 3335741209,
        },
    )

    assert response.status_code == 400
    assert response.content == b"Invalid signature"


def test_get_signature_handles_incorrect_padding(rf):
    signature = "MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q"

    request = rf.get(
        path="/admob-ssv/",
        data={"signature": signature},
    )

    with pytest.raises(binascii.Error):
        base64.urlsafe_b64decode(signature)

    AdmobSSVView().get_signature(request)


def test_get_unverified_content(rf):
    request = rf.get(
        path="/admob-ssv/",
        data={
            "ad_network": 5450213213286189855,
            "ad_unit": 1234567890,
            "custom_data": "TEMPERED CUSTOM DATA",
            "reward_amount": 1,
            "reward_item": "Reward",
            "timestamp": 1683852940453,
            "transaction_id": 123456789,
            "user_id": "userid42",
            "signature": "MEQCIAhKY5P-aBmjU0iqxtjq2JPzeNKnQ92ZbSPC33Sp4ByeAiBArqhg9_uafB1LCBYVIXWNOW8vVVlocLc81ptROfE44Q",
            "key_id": 3335741209,
        },
    )

    unverified_content = AdmobSSVView().get_unverified_content(request)
    assert (
        unverified_content
        == b"ad_network=5450213213286189855&ad_unit=1234567890&custom_data=TEMPERED+CUSTOM+DATA&reward_amount=1&reward_item=Reward&timestamp=1683852940453&transaction_id=123456789&user_id=userid42"
    )


def test_get_public_key_only_from_cache():
    cache.set("admob_ssv.public_keys", {"TestKeyId": "TestKey"}, 24 * 60 * 60)

    view = AdmobSSVView()
    fetch_public_keys = mock.Mock()
    mock.patch.object(view, "fetch_public_keys", fetch_public_keys)

    public_key = view.get_public_key("TestKeyId")
    assert public_key == "TestKey"
    assert not fetch_public_keys.called


def test_get_public_key_caches_missing_keys():
    cache.delete("admob_ssv.public_keys")

    view = AdmobSSVView()
    public_key = view.get_public_key("3335741209")
    assert public_key == PUBLIC_KEY_PEM
    assert cache.get("admob_ssv.public_keys") == {"3335741209": PUBLIC_KEY_PEM}


def test_get_public_key_handles_unknown_keys():
    view = AdmobSSVView()
    public_key = view.get_public_key("UnknownKeyId")
    assert public_key is None


def test_fetch_public_keys():
    view = AdmobSSVView()
    public_keys = view.fetch_public_keys()
    assert public_keys == {"3335741209": PUBLIC_KEY_PEM}


def test_verify_signature_with_valid_signature():
    signature = b"0D\x02 \x08Jc\x93\xfeh\x19\xa3SH\xaa\xc6\xd8\xea\xd8\x93\xf3x\xd2\xa7C\xdd\x99m#\xc2\xdft\xa9\xe0\x1c\x9e\x02 @\xae\xa8`\xf7\xfb\x9a|\x1dK\x08\x16\x15!u\x8d9o/UYhp\xb7<\xd6\x9bQ9\xf18\xe1"
    content = b"ad_network=5450213213286189855&ad_unit=1234567890&custom_data=customdata42&reward_amount=1&reward_item=Reward&timestamp=1683852940453&transaction_id=123456789&user_id=userid42"

    view = AdmobSSVView()
    assert view.verify_signature(PUBLIC_KEY_PEM, signature, content)


def test_verify_signature_with_invalid_signature():
    signature = b"0D\x02 \x08Jc\x93\xfeh\x19\xa3SH\xaa\xc6\xd8\xea\xd8\x93\xf3x\xd2\xa7C\xdd\x99m#\xc2\xdft\xa9\xe0\x1c\x9e\x02 @\xae\xa8`\xf7\xfb\x9a|\x1dK\x08\x16\x15!u\x8d9o/UYhp\xb7<\xd6\x9bQ9\xf18\xe1"
    content = b"ad_network=5450213213286189855&ad_unit=1234567890&custom_data=TEMPERED_DATA&reward_amount=1&reward_item=Reward&timestamp=1683852940453&transaction_id=123456789&user_id=userid42"

    view = AdmobSSVView()
    assert not view.verify_signature(PUBLIC_KEY_PEM, signature, content)

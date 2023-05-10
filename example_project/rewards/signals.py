from django.dispatch import receiver
from django_admob_ssv.signals import valid_admob_ssv
from .models import Reward


@receiver(valid_admob_ssv)
def reward_user(sender, query, **kwargs):
    ad_network = query.get("ad_network")
    ad_unit = query.get("ad_unit")
    custom_data = query.get("custom_data")
    key_id = query.get("key_id")
    reward_amount = query.get("reward_amount")
    reward_item = query.get("reward_item")
    signature = query.get("signature")
    timestamp = query.get("timestamp")
    transaction_id = query.get("transaction_id")
    user_id = query.get("user_id")

    msg = "Valid SSV! Reward item: {}, Reward amount: {}, User ID: {}"
    print(msg.format(reward_item, reward_amount, user_id))

    Reward.objects.create(
        ad_network=ad_network,
        ad_unit=ad_unit,
        custom_data=custom_data,
        key_id=key_id,
        reward_amount=reward_amount,
        reward_item=reward_item,
        signature=signature,
        timestamp=timestamp,
        transaction_id=transaction_id,
        user_id=user_id,
    )

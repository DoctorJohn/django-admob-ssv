from django.contrib import admin
from .models import Reward


class RewardAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "timestamp",
        "ad_network",
        "ad_unit",
        "reward_item",
        "reward_amount",
        "user_id",
    )
    list_filter = (
        "ad_network",
        "ad_unit",
        "reward_item",
        "reward_amount",
    )
    search_fields = (
        "transaction_id",
        "user_id",
        "custom_data",
        "signature",
    )


admin.site.register(Reward, RewardAdmin)

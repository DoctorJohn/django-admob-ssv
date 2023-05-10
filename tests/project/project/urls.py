from django.contrib import admin
from django.urls import path
from admob_ssv.views import admob_ssv


urlpatterns = [
    path("", admob_ssv),
    path("admin/", admin.site.urls),
]

from django.contrib import admin
from django.urls import path
from django_admob_ssv.views import admob_ssv


urlpatterns = [
    path("", admob_ssv),
    path("admin/", admin.site.urls),
]

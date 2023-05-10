from django.contrib import admin
from django.urls import path
from admob_ssv.views import AdmobSSVView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("admob-ssv", AdmobSSVView.as_view()),
]

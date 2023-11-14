from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from admob_ssv.views import AdmobSSVView

urlpatterns = [
    path("", RedirectView.as_view(url="/admin/")),
    path("admin/", admin.site.urls),
    path("admob-ssv/", AdmobSSVView.as_view()),
]

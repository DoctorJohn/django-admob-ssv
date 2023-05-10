from django.contrib import admin
from django.urls import path
from admob_ssv.views import AdmobSSVView


urlpatterns = [
    path("", AdmobSSVView.as_view()),
    path("admin/", admin.site.urls),
]

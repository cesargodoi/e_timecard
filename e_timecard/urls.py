from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("e_timecard.apps.core.urls", namespace="core")),
    path("admin/", admin.site.urls),
]

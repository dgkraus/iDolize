from django.contrib import admin
from django.urls import path, include

from landing_page.views import IndexView

from debug_toolbar.toolbar import debug_toolbar_urls

app_name = "landing"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
] + debug_toolbar_urls()
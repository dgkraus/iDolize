from django.contrib import admin
from django.urls import path, include

from . import views

from debug_toolbar.toolbar import debug_toolbar_urls

app_name = "idolize"

urlpatterns = [
    path("", views.idol_search, name="idol_search"),
    path('admin/', admin.site.urls),
] + debug_toolbar_urls()
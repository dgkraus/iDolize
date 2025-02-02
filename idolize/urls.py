from django.contrib import admin
from django.urls import path, include

from . import views

from debug_toolbar.toolbar import debug_toolbar_urls

app_name = "idolize"

urlpatterns = [
    path("", views.IdolSearch.as_view(), name="idol_search"),
    path("<int:pk>/", views.IdolProfileView.as_view(), name="idol-profile"),
    path("api/idols/", views.IdolList.as_view(), name="idol-list"),
    path('admin/', admin.site.urls),
] + debug_toolbar_urls()
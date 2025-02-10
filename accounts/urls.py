from django.contrib import admin
from django.urls import path, include

from . import views

from debug_toolbar.toolbar import debug_toolbar_urls

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
] + debug_toolbar_urls()
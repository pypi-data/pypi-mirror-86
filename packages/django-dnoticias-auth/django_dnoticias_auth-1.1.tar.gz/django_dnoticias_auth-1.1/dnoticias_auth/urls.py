from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('silent-check-sso/', views.SilentCheckSSOView.as_view(), name="silent-check-sso"),
    path('login/', views.LoginView.as_view(), name="login"),
]
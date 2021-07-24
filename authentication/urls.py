from django import views
from .views import RegistrationView
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('register', RegistrationView.as_view(), name = "register" ),
]

from django import views
from .views import CompletePasswordReset, EmailValidationView, LogoutView, RegistrationView, UsernameValidationView, VarificationView, LoginView, ResetPasswordView
from django.urls import path
from django.urls.conf import include
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name = 'register' ),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name = 'validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name = 'validate-email'),
    path('activate/<uidb64>/<token>', VarificationView.as_view(), name = 'activate'),
    path('login', LoginView.as_view(), name = 'login' ),
    path('logout', LogoutView.as_view(), name = 'logout' ),
    path('reset-password', ResetPasswordView.as_view(), name = 'reset-password'),
    path('reset-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name = 'reset-new-password'),
]

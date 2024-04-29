from django.urls import path
from .views import RegisterPageView, LoginView, ActivateCodeView, ForgotPasswordView, ResetPasswordView, LogoutView

urlpatterns = [
    path('register', RegisterPageView.as_view(), name='register_page'),
    path('login', LoginView.as_view(), name='login_page'),
    path('logout', LogoutView.as_view(), name='logout_page'),
    path('forget-pass', ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('reset-pass/<active_code>', ResetPasswordView.as_view(), name='reset_password_page'),
    path('activate-account/<email_active_code>', ActivateCodeView.as_view(), name='activate_account'),
    path('forget-pass', ForgotPasswordView.as_view(), name='forgot_password_page'),


]

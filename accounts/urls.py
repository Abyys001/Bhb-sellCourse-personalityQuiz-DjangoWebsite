# accounts/urls.py

from django.urls import path
from .views import register_view, login_view, logout_view, account_view, user_dashboard

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("account/", account_view, name="account"), 
    path("dashboard/", user_dashboard, name="dashboard"),
]

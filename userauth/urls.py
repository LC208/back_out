from django.urls import path

from userauth.views import (
    UserAuthView,
    CookieTokenRefreshView,
    UserLogOutView,
)

urlpatterns = [
    path("", UserAuthView.as_view(), name="auth"),
    path("refresh", CookieTokenRefreshView.as_view()),
    path("log_out", UserLogOutView.as_view()),
]

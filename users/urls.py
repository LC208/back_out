from django.urls import path

from users.views import (
    UserCreateView,
    UserInfoView,
    UserCompanyView,
    UserPracticeListCreateView,
    UserPracticeSingleView,
)

urlpatterns = [
    path("add", UserCreateView.as_view(), name="user_add"),
    path("info", UserInfoView.as_view()),
    path("company", UserCompanyView.as_view()),
    path("practice", UserPracticeListCreateView.as_view()),
    path("practice/<int:pk>", UserPracticeSingleView.as_view()),
]

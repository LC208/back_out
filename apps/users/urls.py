from django.urls import path

from apps.users.views import (
    UserCreateView,
    UserInfoView,
    UserCompanyView,
    UserPracticeListCreateView,
    UserPracticeSingleView,
    UserThemeListCreateView,
    UserThemeDeleteUpdateView,
    UserThemePracticeDeleteCreateView,
    UserContactListCreateView,
    UserContactDeleteUpdateView,
    UserContactPracticeDeleteCreateView,
)

urlpatterns = [
    path("add", UserCreateView.as_view(), name="user_add"),
    path("info", UserInfoView.as_view()),
    path("company", UserCompanyView.as_view()),
    path("practice", UserPracticeListCreateView.as_view()),
    path("practice/<int:pk>", UserPracticeSingleView.as_view()),
    path("themes", UserThemeListCreateView.as_view()),
    path("themes/<int:pk>", UserThemeDeleteUpdateView.as_view()),
    path(
        "practice/<int:pk>/themes/<int:theme>",
        UserThemePracticeDeleteCreateView.as_view(),
    ),
    path("contact", UserContactListCreateView.as_view()),
    path("contact/<int:pk>", UserContactDeleteUpdateView.as_view()),
    path(
        "practice/<int:pk>/contact/<int:contact>",
        UserContactPracticeDeleteCreateView.as_view(),
    ),
]

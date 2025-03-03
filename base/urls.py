from django.urls import path

from base.views import (
    DocLinkCreateView,
    PracticesList,
    PracticeCreateView,
    SpecialityCreateView,
    ThemeCreateView,
    SpecialitySingleView,
    SpecialityList,
    PracticeSingleView,
    UserAuthView,
    UserCreateView,
    UserLogOutView,
    CompanySingleViewByToken,
    CookieTokenRefreshView, ThemeSingleView, ThemeListView,UserInfoView,UserCompanyView,UserPracticeListCreateView,UserPracticeSingleView
)

urlpatterns = [

    path("practice/<int:pk>", PracticeSingleView.as_view(), name="practice_single"),
    path("theme/", ThemeListView.as_view(), name="theme_list"),
    path("theme/add", ThemeCreateView.as_view(), name="theme_add"),
    path("theme/<int:pk>", ThemeSingleView.as_view(), name="theme_single"),
    path("speciality/", SpecialityList.as_view(), name="speciality_list"),
    path("speciality/add", SpecialityCreateView.as_view(), name="speciality_add"),
    path("speciality/<int:pk>", SpecialitySingleView.as_view(), name="speciality_single"),
    path("doclinks/add", DocLinkCreateView.as_view(), name="doclinks_add"),
    path("auth/", UserAuthView.as_view(), name="auth"),
    path("user/add", UserCreateView.as_view(), name="user_add"),
    path("auth/refresh", CookieTokenRefreshView.as_view()),
    path("auth/log_out",UserLogOutView.as_view()),
    path("user/info",UserInfoView.as_view()),
    path("user/company",UserCompanyView.as_view()),
    path("user/practice",UserPracticeListCreateView.as_view()),
    path("user/practice/<int:pk>",UserPracticeSingleView.as_view()),
]

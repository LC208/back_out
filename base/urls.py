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
    CookieTokenRefreshView,
)

urlpatterns = [

    path("practice/", PracticesList.as_view(), name="practice_list"),
    path("practice/add", PracticeCreateView.as_view(), name="practice_add"),
    path("practice/<int:pk>", PracticeSingleView.as_view(), name="practice_single"),
    path("theme/add", ThemeCreateView.as_view(), name="company_add"),
    path("speciality/add", SpecialityCreateView.as_view(), name="speciality_add"),
    path("speciality/", SpecialityList.as_view(), name="speciality_list"),
    path("speciality/<int:pk>", SpecialitySingleView.as_view(), name="speciality_single"),
    path("doclinks/add", DocLinkCreateView.as_view(), name="doclinks-add"),
    path("auth/", UserAuthView.as_view(), name="auth"),
    path("user/add", UserCreateView.as_view(), name="user_add"),
    path("auth/refresh", CookieTokenRefreshView.as_view()),
    path("auth/log_out",UserLogOutView.as_view()),
    path("user/info",CompanySingleViewByToken.as_view()),

]

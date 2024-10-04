from django.urls import path

from base.views import (
    DocLinkCreateView,
    PracticesList,
    PracticeCreateView,
    SpecilityCreateView,
    ThemeCreateView,
    SpecialitySingleView,
    SpecialityList,
    PracticeSingleView,
    UserAuthView,
    UserCreateView,
    CompanyFullListView,
)

urlpatterns = [

    path("practice/", PracticesList.as_view(), name="practice_list"),
    path("practice/add", PracticeCreateView.as_view(), name="practice_add"),
    path("practice/<int:pk>", PracticeSingleView.as_view(), name="practice_single"),
    path("theme/add", ThemeCreateView.as_view(), name="company_add"),
    path("speciality/add", SpecilityCreateView.as_view(), name="speciality_add"),
    path("speciality/", SpecialityList.as_view(), name="speciality_list"),
    path("speciality/<int:pk>", SpecialitySingleView.as_view(), name="speciality_single"),
    path("doclinks/add", DocLinkCreateView.as_view(), name="doclinks-add"),
    path("auth/", UserAuthView.as_view(), name="auth"),
    path("user/add", UserCreateView.as_view(), name="user-add"),
    path("company/full", CompanyFullListView.as_view(), name="company_list"),

]

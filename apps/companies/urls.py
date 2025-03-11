from django.urls import path

from apps.companies.views import (
    CompanyListView,
    CompanyCreateView,
    CompanySingleView,
)


urlpatterns = [
    path("", CompanyListView.as_view(), name="company_list"),
    path("add", CompanyCreateView.as_view(), name="company_add"),
    path("<int:pk>", CompanySingleView.as_view(), name="company_list"),
]

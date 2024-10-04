from django.urls import path


from olddb.views import (
    FacultyList,
    FacultyCreateView,
    FacultySingleView,
    CompanyListView,
    CompanyCreateView,
    CompanySingleView,
)
urlpatterns = [
    path("faculty/", FacultyList.as_view(), name="faculty_list"),
    path("faculty/add", FacultyCreateView.as_view(), name="faculty_add"),
    path("faculty/<int:pk>", FacultySingleView.as_view(), name="faculty_single"),
    path("company/", CompanyListView.as_view(), name="company_list"),
    path("company/add", CompanyCreateView.as_view(), name="company_add"),
    path("company/<int:pk>", CompanySingleView.as_view(), name="company_list"),
]

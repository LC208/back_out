from django.urls import path

from apps.faculties.views import (
    FacultyList,
    FacultyCreateView,
    FacultySingleView,
)

urlpatterns = [
    path("", FacultyList.as_view(), name="faculty_list"),
    path("add", FacultyCreateView.as_view(), name="faculty_add"),
    path("<int:pk>", FacultySingleView.as_view(), name="faculty_single"),
]

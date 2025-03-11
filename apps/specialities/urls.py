from django.urls import path

from apps.specialities.views import (
    SpecialityList,
    SpecialityCreateView,
    SpecialitySingleView,
)

urlpatterns = [
    path("", SpecialityList.as_view(), name="speciality_list"),
    path("add", SpecialityCreateView.as_view(), name="speciality_add"),
    path("<int:pk>", SpecialitySingleView.as_view(), name="speciality_single"),
]

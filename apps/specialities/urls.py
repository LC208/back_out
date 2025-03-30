from django.urls import path

from apps.specialities.views import (
    SpecialityList,
    SpecialityCreateView,
    SpecialitySingleView,
    DirectionList,
)

urlpatterns = [
    path("", SpecialityList.as_view(), name="speciality_list"),
    path("add", SpecialityCreateView.as_view(), name="speciality_add"),
    path("<int:pk>", SpecialitySingleView.as_view(), name="speciality_single"),
    # path("streams", StreamList.as_view(), name="stream_list"),
]

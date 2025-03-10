from django.urls import path

from practices.views import PracticeSingleView, PracticeListView


urlpatterns = [
    path("<int:pk>", PracticeSingleView.as_view(), name="practice_single"),
    path("", PracticeListView.as_view(), name="practice_list"),
]

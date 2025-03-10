from django.urls import path

from themes.views import (
    ThemeListView,
    ThemeCreateView,
    ThemeSingleView,
)

urlpatterns = [
    path("", ThemeListView.as_view(), name="theme_list"),
    path("add", ThemeCreateView.as_view(), name="theme_add"),
    path("<int:pk>", ThemeSingleView.as_view(), name="theme_single"),
]

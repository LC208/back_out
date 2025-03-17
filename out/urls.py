from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/out/base/auth/", include("apps.userauth.urls")),
    path("api/out/base/user/", include("apps.users.urls")),
    path("api/out/base/speciality/", include("apps.specialities.urls")),
    path("api/out/base/practice/", include("apps.practices.urls")),
    path("api/out/base/contacts/", include("apps.contacts.urls")),
    path("api/out/base/theme/", include("apps.themes.urls")),
    path("api/out/legacy/company/", include("apps.companies.urls")),
    path("api/out/legacy/faculty/", include("apps.faculties.urls")),
]

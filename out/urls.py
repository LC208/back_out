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
    path("api/out/base/auth/", include("userauth.urls")),
    path("api/out/base/user/", include("users.urls")),
    path("api/out/base/speciality/", include("specialities.urls")),
    path("api/out/base/practice/", include("practices.urls")),
    path("api/out/base/doclinks/", include("doclinks.urls")),
    path("api/out/base/theme/", include("themes.urls")),
    path("api/out/base/company/", include("companies.urls")),
    path("api/out/base/faculty/", include("faculties.urls")),
]

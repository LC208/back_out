from django.urls import path

from apps.doclinks.views import DocLinkCreateView

urlpatterns = [
    path("add", DocLinkCreateView.as_view(), name="doclinks_add"),
]

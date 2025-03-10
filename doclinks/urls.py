from django.urls import path

from doclinks.views import DocLinkCreateView

urlpatterns = [
    path("add", DocLinkCreateView.as_view(), name="doclinks_add"),
]

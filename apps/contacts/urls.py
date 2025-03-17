from django.urls import path

from apps.contacts.views import ContactCreateView

urlpatterns = [
    path("add", ContactCreateView.as_view(), name="contacts_add"),
]

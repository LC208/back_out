from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.contacts.models import Contact
from apps.contacts.serializers import ContactSerializer


class ContactCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

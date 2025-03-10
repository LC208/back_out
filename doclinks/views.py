from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from doclinks.models import DocLink
from doclinks.serializers import DockLinkSerializer


class DocLinkCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = DocLink.objects.all()
    serializer_class = DockLinkSerializer

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.doclinks.models import DocLink
from apps.doclinks.serializers import DockLinkSerializer


class DocLinkCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = DocLink.objects.all()
    serializer_class = DockLinkSerializer

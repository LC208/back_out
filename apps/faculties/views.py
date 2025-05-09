from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.faculties.models import Faculty
from apps.faculties.serializers import FacultySerializer


class FacultyList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = (
        Faculty.objects.prefetch_related("specialities__direction_set")
        .exclude(image_url__isnull=True)
        .exclude(image_url="")
    )
    serializer_class = FacultySerializer


class FacultyCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultySingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Faculty.objects.exclude(image_url__isnull=True).exclude(image_url="")
    serializer_class = FacultySerializer

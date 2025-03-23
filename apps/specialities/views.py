from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from apps.specialities.models import Speciality, Stream
from apps.specialities.serializers import SpecialitySerializer, StreamSerializer
from django.db.models import Min


class SpecialityCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class SpecialityList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class SpecialitySingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class StreamList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = StreamSerializer

    def get_queryset(self):
        subquery = (
            Stream.objects.values("short_name")
            .annotate(min_id=Min("id"))
            .values("min_id")
        )
        return Stream.objects.filter(id__in=subquery)

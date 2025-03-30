from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from apps.specialities.models import Speciality, Direction
from apps.specialities.serializers import SpecialitySerializer, DirectionSerializer
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


class DirectionList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DirectionSerializer
    queryset = Direction.objects.all()

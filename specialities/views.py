from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from specialities.models import Speciality
from specialities.serializers import SpecialitySerializer


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

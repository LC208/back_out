# Create your views here.
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAdminUser, AllowAny

from base.models import Faculty, Companies
from base.serializers import CompanySerializer, FacultySerializer, CompaniesSerializer

class FacultyList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultyCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultySingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class CompanyListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer


class CompanyCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer


class CompanySingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Companies.objects.prefetch_related("company__themes")
    serializer_class = CompaniesSerializer

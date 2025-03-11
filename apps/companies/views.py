from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.companies.models import Companies
from apps.companies.serializers import CompanySerializer, CompaniesSerializer


class CompanyListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer


class CompanyCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer


class CompanySingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer

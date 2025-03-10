from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from companies.models import Companies
from companies.serializers import CompanySerializer, CompaniesSerializer


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
    queryset = Companies.objects.prefetch_related("company__themes")
    serializer_class = CompaniesSerializer

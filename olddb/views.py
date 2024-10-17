# Create your views here.
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, BasePermission, IsAuthenticated

from olddb.models import Faculty, Companies
# from models import Faculty
from olddb.serializers import CompanySerializer, FacultySerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class FacultyList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultyCreateView(CreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultySingleView(RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAdminUser|ReadOnly]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class CompanyListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer


class CompanyCreateView(CreateAPIView):
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]


class CompanySingleView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser|ReadOnly]
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer

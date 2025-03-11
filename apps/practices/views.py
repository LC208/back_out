from rest_framework.views import APIView
from apps.practices.serializers import PracticeListSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.practices.models import Practice
from django_filters import rest_framework as filters


class PracticeListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Practice.objects.all()
    serializer_class = PracticeListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("faculty",)


class PracticeSingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Practice.objects.all()
    serializer_class = PracticeListSerializer

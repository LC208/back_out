from users.models import AuthsExtendedUser
from users.serializers import UserSerializer
from companies.serializers import CompanySerializer
from practices.serializers import PracticeTrimmedListSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from companies.models import Companies
from practices.models import Practice
from django.shortcuts import get_object_or_404


class UserCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = AuthsExtendedUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserInfoView(RetrieveUpdateAPIView):
    queryset = AuthsExtendedUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user


class UserCompanyView(RetrieveUpdateAPIView):
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return get_object_or_404(Companies, user=self.request.user.id)


class UserPracticeListCreateView(ListCreateAPIView):
    serializer_class = PracticeTrimmedListSerializer

    def get_queryset(self):
        return Practice.objects.filter(company__user=self.request.user)


class UserPracticeSingleView(RetrieveUpdateDestroyAPIView):
    queryset = Practice.objects.all()
    serializer_class = PracticeTrimmedListSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Practice, pk=pk, company__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        self.perform_destroy(instance)
        return Response(data, status=status.HTTP_200_OK)

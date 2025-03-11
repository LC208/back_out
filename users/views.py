from users.models import AuthsExtendedUser
from users.serializers import UserSerializer, UserCreateSerializer
from companies.serializers import CompanySerializer
from practices.serializers import PracticeTrimmedListSerializer
from themes.serializers import ThemeSerializer
from doclinks.serializers import DockLinkSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from rest_framework.views import APIView
from companies.models import Companies
from practices.models import Practice, PracticeThemeRelation, PracticeDocLinkRelation
from themes.models import Theme
from doclinks.models import DocLink
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class UserCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = AuthsExtendedUser.objects.all()
    serializer_class = UserCreateSerializer

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


class UserThemeListCreateView(ListCreateAPIView):
    serializer_class = ThemeSerializer

    def get_queryset(self):
        return Theme.objects.filter(company__user=self.request.user).distinct()

    def perform_create(self, serializer):
        company = get_object_or_404(Companies, user=self.request.user.id)
        theme = serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserThemeDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ThemeSerializer
    http_method_names = ["patch", "delete"]

    def get_object(self):
        return get_object_or_404(
            Theme, pk=self.kwargs["pk"], company__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.practicethemerelation_set.all().delete()
        super().perform_destroy(instance)


class UserThemePracticeDeleteCreateView(APIView):
    def post(self, request, *args, **kwargs):
        practice = get_object_or_404(
            Practice, pk=self.kwargs["pk"], company__user=self.request.user
        )
        theme = get_object_or_404(
            Theme, pk=self.kwargs["theme"], company__user=self.request.user
        )

        existing_relation = PracticeThemeRelation.objects.filter(
            practice=practice, theme=theme
        ).exists()

        if existing_relation:
            return Response(status=status.HTTP_200_OK)

        PracticeThemeRelation.objects.create(practice=practice, theme=theme)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        practice = get_object_or_404(
            Practice, pk=self.kwargs["pk"], company__user=self.request.user
        )
        theme = get_object_or_404(
            Theme, pk=self.kwargs["theme"], company__user=self.request.user
        )

        relation = PracticeThemeRelation.objects.filter(
            practice=practice, theme=theme
        ).first()

        if not relation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        relation.delete()
        return Response(status=status.HTTP_200_OK)


class UserDocLinkListCreateView(ListCreateAPIView):
    serializer_class = DockLinkSerializer

    def get_queryset(self):
        return DocLink.objects.filter(company__user=self.request.user).distinct()

    def perform_create(self, serializer):
        company = get_object_or_404(Companies, user=self.request.user.id)
        doclink = serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDocLinkDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = DockLinkSerializer
    http_method_names = ["patch", "delete"]

    def get_object(self):
        return get_object_or_404(
            DocLink, pk=self.kwargs["pk"], company__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.practicedoclinkrelation_set.all().delete()
        super().perform_destroy(instance)


class UserDocLinkPracticeDeleteCreateView(APIView):
    def post(self, request, *args, **kwargs):
        practice = get_object_or_404(
            Practice, pk=self.kwargs["pk"], company__user=self.request.user
        )
        doclink = get_object_or_404(
            DocLink, pk=self.kwargs["doclink"], company__user=self.request.user
        )

        existing_relation = PracticeDocLinkRelation.objects.filter(
            practice=practice, contact=doclink
        ).exists()

        if existing_relation:
            return Response(status=status.HTTP_200_OK)

        PracticeDocLinkRelation.objects.create(practice=practice, contact=doclink)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        practice = get_object_or_404(
            Practice, pk=self.kwargs["pk"], company__user=self.request.user
        )
        doclink = get_object_or_404(
            DocLink, pk=self.kwargs["doclink"], company__user=self.request.user
        )

        relation = PracticeDocLinkRelation.objects.filter(
            practice=practice, contact=doclink
        ).first()

        if not relation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        relation.delete()
        return Response(status=status.HTTP_200_OK)

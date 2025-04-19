from apps.users.models import AuthsExtendedUser
from apps.users.serializers import UserSerializer, UserCreateSerializer
from apps.companies.serializers import CompanySerializer, YearMetaCompanySerializer
from apps.practices.serializers import PracticeTrimmedListSerializer
from apps.themes.serializers import ThemeSerializer
from apps.contacts.serializers import ContactSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from rest_framework.views import APIView
from apps.companies.models import Companies, YearMetaCompany
from apps.practices.models import (
    Practice,
    PracticeThemeRelation,
    PracticeContactRelation,
)
from apps.themes.models import Theme
from apps.contacts.models import Contact
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin


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


class UserCompanyMetaListCreateView(ListCreateAPIView):
    serializer_class = YearMetaCompanySerializer

    def get_queryset(self):
        return YearMetaCompany.objects.filter(
            company__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        company = get_object_or_404(Companies, user=self.request.user.id)
        ymc = serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserCompanyMetaDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = YearMetaCompanySerializer
    http_method_names = ["patch", "delete"]

    def get_object(self):
        return get_object_or_404(
            YearMetaCompany, pk=self.kwargs["pk"], company__user=self.request.user
        )


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
    serializer_class = None

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


class UserContactListCreateView(ListCreateAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(company__user=self.request.user).distinct()

    def perform_create(self, serializer):
        company = get_object_or_404(Companies, user=self.request.user.id)
        Contact = serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserContactDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    http_method_names = ["patch", "delete"]

    def get_object(self):
        return get_object_or_404(
            Contact, pk=self.kwargs["pk"], company__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.practicecontactrelation_set.all().delete()
        super().perform_destroy(instance)


class UserContactPracticeDeleteCreateView(APIView):
    serializer_class = None

    def post(self, request, *args, **kwargs):
        practice = get_object_or_404(
            Practice, pk=self.kwargs["pk"], company__user=self.request.user
        )
        contact = get_object_or_404(
            Contact, pk=self.kwargs["contact"], company__user=self.request.user
        )

        existing_relation = PracticeContactRelation.objects.filter(
            practice=practice, contact=contact
        ).exists()

        if existing_relation:
            return Response(status=status.HTTP_200_OK)

        PracticeContactRelation.objects.create(practice=practice, contact=contact)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        practice = get_object_or_404(
            Practice, pk=self.kwargs["pk"], company__user=self.request.user
        )
        contact = get_object_or_404(
            Contact, pk=self.kwargs["contact"], company__user=self.request.user
        )

        relation = PracticeContactRelation.objects.filter(
            practice=practice, contact=contact
        ).first()

        if not relation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        relation.delete()
        return Response(status=status.HTTP_200_OK)

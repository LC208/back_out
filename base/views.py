from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView
)
from rest_framework.response import Response

from base.models import Practice, DocLink, Speciality, Theme
from base.serializers import DockLinkSerializer, CompanyFullSerializer
from base.serializers import (
    PracticeAddSerializer,
    PracticeListSerializer,
    ThemeSerializer,
    SpecialitySerializer,
    UserSerializer,
    AuthSerializer,
)
from olddb.models import Companies


# Create your views here.


class SpecilityCreateView(CreateAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class CompanyFullListView(ListAPIView):
    queryset = Companies.objects.all()
    serializer_class = CompanyFullSerializer


class SpecialityList(ListAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class SpecialitySingleView(RetrieveUpdateDestroyAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class PracticeCreateView(CreateAPIView):
    queryset = Practice.objects.all()
    serializer_class = PracticeAddSerializer


class PracticesList(ListAPIView):
    queryset = Practice.objects.all()
    serializer_class = PracticeListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("faculty",)


class PracticeSingleView(RetrieveUpdateDestroyAPIView):
    queryset = Practice.objects.all()
    serializer_class = PracticeListSerializer


class DocLinkCreateView(CreateAPIView):
    queryset = DocLink.objects.all()
    serializer_class = DockLinkSerializer


class ThemeCreateView(CreateAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserAuthView(GenericAPIView):
    serializer_class = AuthSerializer

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"error": "Wrong credentials"}, status=400)

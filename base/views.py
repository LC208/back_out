from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
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
    LogOutSerializer,
)
from olddb.models import Companies
from rest_framework_simplejwt.tokens import RefreshToken


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
    permission_classes = [AllowAny]

    def post(self, request):

        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username
            })
            data = {'refresh' : str(refresh) , 'access': str(refresh.access_token)}
            return Response(data)
        else:
            return Response({"error": "Wrong credentials"})

class UserLogOutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogOutSerializer
    def post(self,request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error':'Required refresh token'},status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Invalid Refresh token'},status=status.HTTP_400_BAD_REQUEST)
        return Response ({'success':'Success log out'},status=status.HTTP_200_OK)
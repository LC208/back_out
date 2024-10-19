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
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
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
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication




# Create your views here.


class SpecilityCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class CompanyFullListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Companies.objects.all()
    serializer_class = CompanyFullSerializer


class SpecialityList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class SpecialitySingleView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser|IsAuthenticated]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class PracticeCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Practice.objects.all()
    serializer_class = PracticeAddSerializer


class PracticesList(ListAPIView):
    queryset = Practice.objects.all()
    serializer_class = PracticeListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("faculty",)


class PracticeSingleView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser|IsAuthenticated]
    queryset = Practice.objects.all()
    serializer_class = PracticeListSerializer


class DocLinkCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = DocLink.objects.all()
    serializer_class = DockLinkSerializer


class ThemeCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class UserCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
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

class CompamySingleViewByToken(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request):
        access_token_raw = request.data.get('access_token')
        access_token = AccessToken(access_token_raw)
        user_id = access_token.payload["user_id"]
        user_selected = User.objects.get(id=user_id)
        if user_selected is None:
            return Response({'error': 'User not found'},status=status.HTTP_400_BAD_REQUEST)
        compamy_selected = Companies.objects.get(user=user_selected)
        if compamy_selected is None:
            return Response({'error': 'Company related to current user not found'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'username': user_selected.username,
                         'email':user_selected.email,
                         'first_name':user_selected.first_name,
                         'last_name':user_selected.last_name,
                         'company_name':compamy_selected.name,
                         'company_image':compamy_selected.image,
                         },status=status.HTTP_200_OK)
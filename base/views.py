from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from base.models import Practice, DocLink, Speciality, Theme, Companies, CompanyRepresentativeProfile
from base.serializers import DockLinkSerializer, UserProfileEditSerializer, PracticeNoIdSerializer
from base.serializers import (
    PracticeAddSerializer,
    PracticeListSerializer,
    ThemeSerializer,
    SpecialitySerializer,
    UserSerializer,
    AuthSerializer,
    CompanySerializer,
    PracticeTrimmedListSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from drf_spectacular.utils import extend_schema

from itertools import chain
from django.shortcuts import get_object_or_404


# Create your views here.


class SpecialityCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer




class SpecialityList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class SpecialitySingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer

'''
class PracticeCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Practice.objects.all()
    serializer_class = PracticeAddSerializer
'''
class PracticeCreateView(APIView):
    serializer_class = PracticeNoIdSerializer
    def post(self, request):
        select_company = Companies.objects.filter(user=request.user.id)
        if len(select_company)==1:
            serializer = PracticeNoIdSerializer(data=request.data,context={'company':select_company[0].id})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'description':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class PracticesList(ListAPIView):
    permission_classes=[AllowAny]
    queryset = Practice.objects.all()
    serializer_class = PracticeListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("faculty",)


class PracticeSingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
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

class ThemeSingleView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

class ThemeListView(ListAPIView):
    permission_classes = [AllowAny]
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
            data = {'access': str(refresh.access_token)}
            response = Response(data)
            response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value =  str(refresh),
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'])
            return response
        else:
            return Response({"error": "Wrong credentials"})

class UserLogOutView(GenericAPIView):
    @extend_schema(
        request=None,
        responses=None
    )
    def post(self,request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        if not refresh_token:
            return Response({'error':'Required refresh token'},status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Invalid Refresh token'},status=status.HTTP_400_BAD_REQUEST)
        return Response (status=status.HTTP_200_OK)


class CookieTokenRefreshView(TokenRefreshView):
    @extend_schema(
        request=None,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'access': {
                        'type': 'string',
                        'description': 'Access token',
                    }
                },
            }
        },
    )
    def post(self, request, *args, **kwargs):
        # Извлечение токена из cookie
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        
        if not refresh_token:
            raise AuthenticationFailed('Refresh token not found in cookies.')

        # Форматирование данных для обновления токена
        data = {
            'refresh': refresh_token
        }

        # Вызов метода родительского класса для обновления токена
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            data = {'access': serializer.validated_data['access']}
            response = Response(data, status=status.HTTP_200_OK)
            response.set_cookie(
                        key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                        value =  str(serializer.validated_data['refresh']),
                        expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                        secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                        httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                        samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'])
            return response
        except Exception:
            return Response({'error': 'Refresh token blacklisted'},status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch']
        
    def get_object(self):
        return self.request.user

class UserCompanyView(RetrieveUpdateAPIView):
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get', 'patch']
        
    def get_object(self):
        return get_object_or_404(Companies, user=self.request.user.id)

class UserPracticeListCreateView(ListCreateAPIView):
    serializer_class = PracticeTrimmedListSerializer

    def get_queryset(self):
        return Practice.objects.filter(company__user=self.request.user)

class UserPracticeSingleView(RetrieveUpdateDestroyAPIView):
    queryset = Practice.objects.all()
    serializer_class = PracticeTrimmedListSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Practice, pk=pk, company__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        self.perform_destroy(instance)
        return Response(data, status=status.HTTP_200_OK)

# class UserPracticeThemeCreate(CreateAPIView):

# class UserPracticeDocLinkCreate(CreateAPIView):

# class UserPracticeTheme(RetrieveUpdateDestroyAPIView):
#     http_method_names = ['patch', 'delete']

# class UserPracticeDocLink(RetrieveUpdateDestroyAPIView):
#     http_method_names = ['patch', 'delete']

class CompanySingleViewByToken(APIView):
    @extend_schema(
        request=None,
        responses=UserProfileEditSerializer()
    )
    def post(self, request):
        inp = {}
        user_selected = User.objects.filter(id=request.user.id)
        if user_selected is None:
            return Response({'error': 'User not found'},status=status.HTTP_401_UNAUTHORIZED)
        inp = inp | {'user' : user_selected[0]}
        company_selected = Companies.objects.filter(user=request.user.id)
        if len(company_selected) == 1:
            inp = inp | {'company' : company_selected[0]}
            practices_selected = Practice.objects.filter(company=company_selected[0].id)
            if len(practices_selected) > 0:
                inp = inp | {'practices' : practices_selected}
        crp_selected = CompanyRepresentativeProfile.objects.filter(user=request.user.id)
        if len(crp_selected) == 1:
            inp = inp | {'company_representative_profile' : crp_selected[0]}
        serializer = UserProfileEditSerializer(inp)
        return Response(serializer.data,status=status.HTTP_200_OK)
    @extend_schema(
        request=UserProfileEditSerializer(),
        responses=None
    )
    def patch(self, request):
        if not any(key in request.data for key in ['practices', 'company', 'user', 'company_representative_profile']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        if not refresh_token:
            raise AuthenticationFailed('Refresh token not found in cookies.')
        inst = User.objects.filter(id=request.user.id)
        if inst is None:
            return Response({'error': 'User not found'},status=status.HTTP_401_UNAUTHORIZED)
        company_selected = Companies.objects.filter(user=request.user.id)
        out = list(chain(inst, company_selected, Practice.objects.filter(company=company_selected[0].id), CompanyRepresentativeProfile.objects.filter(user=request.user.id)))
        if inst[0].username == request.data['user']['username'] :
            request.data['user'].pop('username')
        serializer = UserProfileEditSerializer(out,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
        return Response(status=status.HTTP_200_OK)
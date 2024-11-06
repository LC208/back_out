from os import access

from rest_framework import status, serializers
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

from base.models import Practice, DocLink, Speciality, Theme, Companies, CompanyRepresentativeProfile
from base.serializers import DockLinkSerializer, UserEditSerializer
from base.serializers import (
    PracticeAddSerializer,
    PracticeListSerializer,
    ThemeSerializer,
    SpecialitySerializer,
    UserSerializer,
    AuthSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from drf_spectacular.utils import extend_schema




# Create your views here.


class SpecilityCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer




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
    permission_classes=[AllowAny]
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
        return Response ({'success':'Success log out'},status=status.HTTP_200_OK)


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

class CompanySingleViewByToken(APIView):
    @extend_schema(
        request=None,
        responses=None
    )
    def post(self,request):
        user_selected = User.objects.get(id=request.user.id)
        if user_selected is None:
            return Response({'error': 'User not found'},status=401)
        data_output = {  'user_id':user_selected.id,
                         'username': user_selected.username,
                         'email':user_selected.email,
                         'first_name':user_selected.first_name,
                         'last_name':user_selected.last_name,
                         }
        company_selected = Companies.objects.filter(user=request.user.id)
        if company_selected.exists():
            company_selected = Companies.objects.get(user=request.user.id)
            all_practics = []
            all_practics_dir = {}
            all_docs_dir = {}
            #нахождение всех практик
            for practica in Practice.objects.all():
                if practica.company.id == company_selected.id:
                    all_practics.append(practica)
            for p in all_practics:
                all_practics_dir.update({'practice_id':p.id,'practice_name':p.name,'practice_faculty':p.faculty.id})
            #нахождение всех доклинков, при условии сущестовании практик
            if all_practics:
                all_docs = []
                for pract in all_practics:
                    for doc in DocLink.objects.all():
                        if doc.practice.id == pract.id:
                            all_docs.append(doc)
                for d in all_docs:
                    all_docs_dir.update({'doclink_id':d.id,'doclink_type':d.type,'doclink_url':d.url})
            data_output = data_output|{'company_id':company_selected.id,
                        'company_name': company_selected.name,
                         'company_image': company_selected.image,
                         'area_of_activity': company_selected.area_of_activity,
                         }|all_practics_dir|all_docs_dir
        company_representative_profile_selected = CompanyRepresentativeProfile.objects.filter(user=request.user.id)
        if company_representative_profile_selected.exists():
            company_representative_profile_selected = CompanyRepresentativeProfile.objects.get(user=request.user.id)
            data_output = data_output|{'job_title':company_representative_profile_selected.job_title,}
        return Response(data=data_output,status=200)
    @extend_schema(
        request=UserEditSerializer,
        responses=None
    )
    def patch(self, request):
        user_data = request.data.get('users')
        User.objects.filter(id=request.user.id).update(**user_data)
        company_selected = Companies.objects.filter(user=request.user.id)
        if company_selected.exists() and 'company' in request.data:
            company_data = request.data.get('company')
            Companies.objects.filter(user=request.user.id).update(**company_data)
        elif not company_selected.exists():
            return Response(status=404)
        company_profile_selected = CompanyRepresentativeProfile.objects.filter(user=request.user.id)
        if company_profile_selected.exists() and 'company_representative_profile' in request.data:
            company_profile_data = request.data.get('company_representative_profile')
            CompanyRepresentativeProfile.objects.filter(user=request.user.id).update(**company_profile_data)
        elif not company_profile_selected.exists():
            return Response(status=404)
        return Response(status=200)
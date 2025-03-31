from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import GenericAPIView
from apps.companies.models import Companies
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from drf_spectacular.utils import extend_schema
from apps.userauth.serializers import AuthSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status


class UserAuthView(GenericAPIView):
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user and Companies.objects.filter(user=user.id).first():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            remember_me = serializer.validated_data.get("rememberMe", False)

            data = {"rememberMe": remember_me}
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({"user_id": user.id, "username": user.username})
            data["access"] = str(refresh.access_token)
            response = Response(data)
            if remember_me:
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=str(refresh),
                    max_age=int(
                        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
                    ),
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
            return response
        else:
            return Response({"error": "Wrong credentials"})


class UserLogOutView(GenericAPIView):
    @extend_schema(request=None, responses=None)
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        if not refresh_token:
            return Response(
                {"error": "Required refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(
                {"error": "Invalid Refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_200_OK)


class CookieTokenRefreshView(TokenRefreshView):
    @extend_schema(
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access": {
                        "type": "string",
                        "description": "Access token",
                    }
                },
            }
        },
    )
    def post(self, request, *args, **kwargs):
        # Извлечение токена из cookie
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])

        if not refresh_token:
            raise AuthenticationFailed("Refresh token not found in cookies.")

        # Форматирование данных для обновления токена
        data = {"refresh": refresh_token}

        # Вызов метода родительского класса для обновления токена
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            data = {"access": serializer.validated_data["access"]}
            response = Response(data, status=status.HTTP_200_OK)
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=str(serializer.validated_data["refresh"]),
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            return response
        except Exception:
            return Response(
                {"error": "Refresh token blacklisted"},
                status=status.HTTP_400_BAD_REQUEST,
            )

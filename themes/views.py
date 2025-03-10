from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from themes.models import Theme
from themes.serializers import ThemeSerializer


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

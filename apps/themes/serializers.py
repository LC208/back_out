from rest_framework import serializers
from apps.themes.models import Theme


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ["id", "title", "type"]

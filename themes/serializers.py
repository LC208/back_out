from rest_framework import serializers
from themes.models import Theme


class ThemeSerializer(serializers.ModelSerializer):
    practice_id = serializers.IntegerField(source="practice.id", read_only=True)

    class Meta:
        model = Theme
        fields = ["id", "title", "practice_id"]


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ["id", "title"]

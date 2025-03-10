from rest_framework import serializers
from themes.models import Theme


class ThemeSerializer(serializers.ModelSerializer):
    practice_id = serializers.IntegerField(source="practice.id", read_only=True)

    class Meta:
        model = Theme
        fields = ["id", "name", "practice_id"]


class ThemeNoIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        exclude = ["id", "practice"]
        write_only_fields = ("company",)


class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = "__all__"
        write_only_fields = ("company",)


class ThemeTrimmedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Theme
        exclude = ["practices"]
        write_only_fields = ("company",)

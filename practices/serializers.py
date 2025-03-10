from rest_framework import serializers
from practices.models import Practice
from companies.models import Companies
from companies.serializers import CompanySerializer
from doclinks.serializers import (
    DockLinkNoIdSerializer,
    DockLinkSerializer,
    DockLinkTrimmedSerializer,
)
from themes.serializers import (
    ThemeNoIdSerializer,
    ThemeSerializer,
    ThemeTrimmedSerializer,
)
from django.shortcuts import get_object_or_404


class PracticeNoIdSerializer(serializers.ModelSerializer):
    themes = ThemeNoIdSerializer(many=True)
    doc_links = DockLinkNoIdSerializer(many=True)

    class Meta:
        model = Practice
        exclude = ["id", "company"]

    def create(self, validated_data):
        docklink_data = validated_data.pop("doc_links")
        theme_data = validated_data.pop("themes")
        validated_data = validated_data | {
            "company": Companies.objects.filter(id=self.context.get("company"))[0]
        }
        practice_selected = Practice.objects.create(**validated_data)
        for dock in docklink_data:
            DocLink.objects.create(practice=practice_selected, **dock)
        for theme in theme_data:
            Theme.objects.create(practice=practice_selected, **theme)
        return practice_selected


class PracticeListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    doc_links = DockLinkSerializer(many=True)
    themes = ThemeSerializer(many=True)

    class Meta:
        model = Practice
        fields = "__all__"


class PracticeTrimmedListSerializer(serializers.ModelSerializer):
    doc_links = DockLinkTrimmedSerializer(many=True, read_only=True)
    themes = ThemeTrimmedSerializer(many=True, read_only=True)
    faculty_name = serializers.CharField(source="faculty.name", read_only=True)

    class Meta:
        model = Practice
        read_only_fields = ("id",)
        exclude = ["company"]

    def create(self, validated_data):
        request = self.context["request"]
        company = get_object_or_404(Companies, user=request.user.id)
        validated_data["company"] = company
        return super().create(validated_data)

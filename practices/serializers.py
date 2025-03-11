from rest_framework import serializers
from practices.models import Practice, PracticeThemeRelation
from companies.models import Companies
from companies.serializers import CompanySerializer
from doclinks.serializers import DockLinkSerializer
from themes.serializers import ThemeSerializer
from django.shortcuts import get_object_or_404


class PracticeListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    doc_links = DockLinkSerializer(many=True)
    themes = ThemeSerializer(many=True)

    class Meta:
        model = Practice
        fields = "__all__"


class PracticeTrimmedListSerializer(serializers.ModelSerializer):
    doc_links = DockLinkSerializer(many=True, read_only=True)
    themes = ThemeSerializer(many=True, read_only=True)
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

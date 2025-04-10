from rest_framework import serializers
from apps.practices.models import Practice, PracticeThemeRelation
from apps.companies.models import Companies
from apps.companies.serializers import CompanySerializer
from apps.contacts.serializers import ContactSerializer
from apps.themes.serializers import ThemeSerializer
from django.shortcuts import get_object_or_404


class PracticeListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    contacts = ContactSerializer(many=True)
    themes = ThemeSerializer(many=True)

    class Meta:
        model = Practice
        fields = "__all__"


class PracticeTrimmedListSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
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

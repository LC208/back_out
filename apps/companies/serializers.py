from rest_framework import serializers
from apps.companies.models import Companies, YearMetaCompany
from apps.themes.models import Theme
from apps.themes.serializers import ThemeSerializer
from apps.contacts.serializers import ContactSerializer

# from specialities.serializers import SpecialitySerializer


class YearMetaCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = YearMetaCompany
        exclude = ["company"]
        read_only_fields = ("id",)


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Companies
        exclude = ["user"]
        read_only_fields = ("id",)


class CompaniesSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    year_meta_company = YearMetaCompanySerializer(many=True, read_only=True)

    class Meta:
        model = Companies
        fields = "__all__"

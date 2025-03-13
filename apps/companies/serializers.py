from rest_framework import serializers
from apps.companies.models import Companies
from apps.themes.models import Theme
from apps.themes.serializers import ThemeSerializer
from apps.doclinks.serializers import DockLinkSerializer

# from specialities.serializers import SpecialitySerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        exclude = ["user"]
        read_only_fields = ("id",)


class CompaniesSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True, read_only=True)
    doclinks = DockLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Companies
        fields = "__all__"

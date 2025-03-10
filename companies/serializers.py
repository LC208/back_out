from rest_framework import serializers
from companies.models import Companies
from themes.models import Theme
from themes.serializers import ThemeSerializer

# from specialities.serializers import SpecialitySerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        exclude = ["id", "user"]


class CompanyFullSerializer(serializers.ModelSerializer):
    # doc_links = DockLinkSerializer(many=True)
    class Meta:
        model = Companies
        fields = "__all__"


class CompanyTrimmedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        exclude = ["user"]


class CompaniesSerializer(serializers.ModelSerializer):
    themes = serializers.SerializerMethodField()

    class Meta:
        model = Companies
        fields = "__all__"

    def get_themes(self, obj):
        themes = Theme.objects.filter(practices__company=obj)
        return ThemeSerializer(themes, many=True).data

from rest_framework.serializers import ModelSerializer, StringRelatedField

from olddb.models import Companies, Faculty


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"


class FacultySerializer(ModelSerializer):
    specialities = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = "__all__"

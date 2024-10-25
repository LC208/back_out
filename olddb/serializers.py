from rest_framework.serializers import ModelSerializer, StringRelatedField
from base import serializers
from base.models import DocLink, Practice
from base.serializers import DockLinkSerializer, PracticeAddSerializer
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

class DocPractCompSerializer(serializers.ModelSerializer):
    pract_ser = PracticeAddSerializer()
    class Meta:
        model = DocLink
        fields = ["type","url","pract_ser"]
    def create(self, validated_data):
        pract_data = validated_data.pop('pract_ser')
        doc_link = DocLink.objects.create(**validated_data)
        for P_data in pract_data:
            company_data = P_data.pop('pract_ser')
            pract = Practice.objects.create(doc_link=doc_link, **P_data)
            for C_data in company_data:
                Companies.objects.create(pract=pract, **C_data)
        return doc_link
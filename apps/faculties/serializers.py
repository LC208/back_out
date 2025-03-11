from rest_framework import serializers
from apps.faculties.models import Faculty
from apps.specialities.serializers import SpecialitySerializer


class FacultySerializer(serializers.ModelSerializer):
    specialities = SpecialitySerializer(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = "__all__"

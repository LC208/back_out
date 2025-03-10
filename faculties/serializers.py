from rest_framework import serializers
from faculties.models import Faculty
from specialities.serializers import SpecialitySerializer


class FacultySerializer(serializers.ModelSerializer):
    specialities = SpecialitySerializer(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = "__all__"

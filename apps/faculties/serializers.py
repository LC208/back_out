from rest_framework import serializers
from apps.faculties.models import Faculty
from apps.specialities.models import Direction
from apps.specialities.serializers import DirectionSerializer


class FacultySerializer(serializers.ModelSerializer):
    directions = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ["id", "name", "image_url", "ais_id", "directions"]

    def get_directions(self, obj):
        directions = Direction.objects.filter(speciality__faculty=obj)
        return DirectionSerializer(directions, many=True).data

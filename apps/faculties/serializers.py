from rest_framework import serializers
from apps.faculties.models import Faculty
from apps.specialities.models import Stream
from apps.specialities.serializers import StreamSerializer


class FacultySerializer(serializers.ModelSerializer):
    streams = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ["id", "name", "image_url", "ais_id", "streams"]

    def get_streams(self, obj):
        unique_streams = Stream.objects.filter(speciality__faculty=obj).distinct(
            "short_name"
        )
        return StreamSerializer(unique_streams, many=True).data

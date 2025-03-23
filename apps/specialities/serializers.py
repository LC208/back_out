from rest_framework import serializers
from apps.specialities.models import Speciality, Stream


class SpecialityListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        item_mapping = {item.id: item for item in instance}

        updated_items = []
        created_items = []

        for item_data in validated_data:
            item_id = item_data.get("id", None)
            if item_id and item_id in item_mapping:
                item = item_mapping[item_id]
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                updated_items.append(item)
            else:
                created_items.append(Speciality(**item_data))

        Speciality.objects.bulk_update(
            updated_items,
            fields=["code", "faculty", "education_level", "full_name", "url"],
        )

        if created_items:
            Speciality.objects.bulk_create(created_items)

        return instance

    class Meta:
        model = Speciality
        fields = "__all__"


class SpecialitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Speciality
        fields = "__all__"
        list_serializer_class = SpecialityListSerializer


class StreamSerializer(serializers.ModelSerializer):
    speciality_name = serializers.CharField(source="speciality.name", read_only=True)
    speciality_code = serializers.CharField(source="speciality.code", read_only=True)
    faculty = serializers.IntegerField(source="speciality.faculty.id", read_only=True)
    education_level = serializers.IntegerField(
        source="speciality.education_level", read_only=True
    )

    class Meta:
        model = Stream
        fields = [
            "id",
            "short_name",
            "speciality_name",
            "speciality_code",
            "faculty",
            "education_level",
        ]

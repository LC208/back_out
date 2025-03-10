from rest_framework import serializers
from specialities.models import Speciality


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

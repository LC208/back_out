from rest_framework import serializers
from doclinks.models import DocLink


class DockLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocLink
        fields = ["id", "type", "value"]

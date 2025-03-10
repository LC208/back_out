from rest_framework import serializers
from doclinks.models import DocLink


class DockLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocLink
        fields = "__all__"


class DockLinkNoIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocLink
        exclude = ["id", "practice"]


class DockLinkTestSerializer(serializers.ModelSerializer):
    practice = serializers.IntegerField(read_only=True)

    class Meta:
        model = DocLink
        fields = "__all__"


class DockLinkTrimmedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = DocLink
        exclude = ["practices"]

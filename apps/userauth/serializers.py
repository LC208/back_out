from apps.users.models import AuthsExtendedUser
from rest_framework import serializers


class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = AuthsExtendedUser
        fields = [
            "username",
            "password",
            "access",
        ]
        write_only_fields = ("password",)

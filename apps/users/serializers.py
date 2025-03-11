from apps.users.models import AuthsExtendedUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthsExtendedUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]
        read_only_fields = ("username",)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthsExtendedUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

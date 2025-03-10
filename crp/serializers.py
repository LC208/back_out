from rest_framework import serializers
from crp.models import CompanyRepresentativeProfile


class CompanyRepresentativeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRepresentativeProfile
        fields = ["job_title", "email", "messenger"]

import this

from attr.filters import exclude
from rest_framework.serializers import ModelSerializer,CharField,Serializer
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import DocLink, Practice, Speciality, Theme, Companies, CompanyRepresentativeProfile
from olddb.serializers import CompanySerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff",
        ]
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'write_only': True}
        }



class AuthSerializer(ModelSerializer):
    username = serializers.CharField(required=True,write_only=True)
    password = serializers.CharField(required=True,write_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "access",
        ]
        write_only_fields = ("password",)


class DockLinkSerializer(ModelSerializer):
    class Meta:
        model = DocLink
        fields = "__all__"


class PracticeAddSerializer(ModelSerializer):
    class Meta:
        model = Practice
        fields = "__all__"

class SpecialitySerializer(ModelSerializer):

    class Meta:
        model = Speciality
        fields = "__all__"

class ThemeSerializer(ModelSerializer):

    class Meta:
        model = Theme
        fields = '__all__'
        write_only_fields = ('company',)

class PracticeListSerializer(ModelSerializer):
    company = CompanySerializer()
    doc_links = DockLinkSerializer(many=True)
    themes = ThemeSerializer(many=True)
    class Meta:
        model = Practice
        fields = "__all__"

class PracticeSerializer(ModelSerializer):
    company = CharField(required=False)
    class Meta:
        model = Practice
        fields = "__all__"

class DockLinkTestSerializer(ModelSerializer):
    practice = serializers.IntegerField(read_only=True)
    class Meta:
        model = DocLink
        fields = "__all__"

class PracticeTestSerializer(ModelSerializer):
    company = CharField(required=False)
    links = DockLinkTestSerializer(many=True, required=False)
    class Meta:
        model = Practice
        fields = "__all__"

class CompanyPracticeDocLinkSerializer(serializers.ModelSerializer):
    practices = PracticeTestSerializer(many=True, required=False)
    users = UserSerializer(required=False)
    class Meta:
        model = Companies
        fields = ['name','image','agreements','practices','users']

    def create(self, validated_data):
        practices_data = validated_data.pop('practices', [])
        users_data = validated_data.pop('users', [])
        user = User.objects.create(**users_data)
        user.set_password(user.password)
        user.save()
        company = Companies.objects.create(user=user,**validated_data)
        for practice_data in practices_data:
            practice_data["company"]=company
            links_data = practice_data.pop('links', [])
            prac = Practice.objects.create( **practice_data)
            for link_data in links_data:
                DocLink.objects.create(practice=prac, **link_data)
        return company

class CompanyFullSerializer(ModelSerializer):

    #doc_links = DockLinkSerializer(many=True)
    class Meta:
        model = Companies
        fields = "__all__"

class CompanyRepresentativeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRepresentativeProfile
        fields = "__all__"

class UserEditSerializer(serializers.Serializer):
    users = UserSerializer(required=False)
    users.Meta.fields = ["username","email","first_name","last_name"]
    company = CompanySerializer(required=False)
    company.Meta.fields = ["name","image","area_of_activity"]
    company_representative_profile = CompanyRepresentativeProfileSerializer(required=False)
    company_representative_profile.Meta.fields = None
    company_representative_profile.Meta.exclude = ['id','user']




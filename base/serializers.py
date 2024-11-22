from rest_framework.serializers import ModelSerializer,CharField
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import DocLink, Practice, Speciality, Theme, Companies, CompanyRepresentativeProfile,Faculty

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

class DockLinkNoIdSerializer(ModelSerializer):
    class Meta:
        model = DocLink
        exclude = ['id','practice']

class ThemeNoIdSerializer(ModelSerializer):
    class Meta:
        model = Theme
        exclude = ['id','practice']
        write_only_fields = ('company',)

class PracticeAddSerializer(ModelSerializer):
    class Meta:
        model = Practice
        fields = "__all__"

class PracticeNoIdSerializer(ModelSerializer):
    themes = ThemeNoIdSerializer(many=True)
    doc_links = DockLinkNoIdSerializer(many=True)
    class Meta:
        model = Practice
        exclude = ["id","company"]
    def create(self, validated_data):
        docklink_data =  validated_data.pop('doc_links')
        theme_data = validated_data.pop('themes')
        validated_data = validated_data|{'company':Companies.objects.filter(id=self.context.get('company'))[0]}
        practice_selected = Practice.objects.create(**validated_data)
        for dock in docklink_data:
            DocLink.objects.create(practice=practice_selected, **dock)
        for theme in theme_data:
            Theme.objects.create(practice=practice_selected, **theme)
        return practice_selected


class SpecialityListSerializer(serializers.ListSerializer):
    
    def update(self, instance, validated_data):
        item_mapping = {item.id: item for item in instance}

        updated_items = []
        created_items = []

        for item_data in validated_data:
            item_id = item_data.get('id', None)
            if item_id and item_id in item_mapping:
                item = item_mapping[item_id]
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                updated_items.append(item)
            else:
                created_items.append(Speciality(**item_data))

        Speciality.objects.bulk_update(updated_items, fields=['code', 'faculty', 'education_level', 'full_name'])

        if created_items:
            Speciality.objects.bulk_create(created_items)

        return instance

    class Meta:
        model = Speciality
        fields = "__all__"

class SpecialitySerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Speciality
        fields = "__all__"
        list_serializer_class=SpecialityListSerializer


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"


class FacultySerializer(ModelSerializer):
    specialities = SpecialitySerializer(many=True, read_only=True)

    class Meta:
        model = Faculty
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
        fields = ['job_title','email','messenger']



class DockLinkTrimmedSerializer(ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = DocLink
        exclude = ['practice']

class ThemeTrimmedSerializer(ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Theme
        exclude = ['practice']
        write_only_fields = ('company',)

class PracticeTrimmedListSerializer(ModelSerializer):
    id = serializers.IntegerField()
    doc_links = DockLinkTrimmedSerializer(many=True)
    themes = ThemeTrimmedSerializer(many=True)
    class Meta:
        model = Practice
        exclude = ['company']

class UserTrimmedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password"
        ]
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CompanyTrimmedSerializer(ModelSerializer):
    class Meta:
        model = Companies
        exclude = ['user']

class UserProfileEditSerializer(serializers.Serializer):
    practices = PracticeTrimmedListSerializer(required=False, many=True,partial=True)
    company = CompanyTrimmedSerializer(required=False,partial=True)
    user = UserTrimmedSerializer(required=False,partial=True)
    company_representative_profile = CompanyRepresentativeProfileSerializer(required=False,partial=True)

    def update(self, instances, validated_data):
        for instance in instances:
            # Обработка и обновление User
            if isinstance(instance, User):
                user_data = validated_data.get('user', None)
                if user_data:
                    user_serializer = UserTrimmedSerializer(instance, data=user_data, partial=True)
                    if user_serializer.is_valid(raise_exception=True):
                        user_serializer.save()

            # Обработка и обновление Company
            elif isinstance(instance, Companies):
                company_data = validated_data.get('company', None)
                if company_data:
                    company_serializer = CompanyTrimmedSerializer(instance, data=company_data, partial=True)
                    if company_serializer.is_valid(raise_exception=True):
                        company_serializer.save()

            elif isinstance(instance, Practice):
                practices_data = validated_data.get('practices', None)
                if practices_data:
                    for practice_data in practices_data:
                        id = practice_data.pop('id')
                        if id == instance.id:
                            practice_serializer = PracticeTrimmedListSerializer(instance, data=practice_data, partial=True)
                            
                            doc_links_data = practice_data.pop('doc_links', [])
                            themes_data = practice_data.pop('themes', [])
                            practice_data['faculty'] = practice_data['faculty'].id

                            for doc_link_data in doc_links_data:
                                doc_id = doc_link_data.pop('id')
                                doc_inst = DocLink.objects.get(id=doc_id, practice=instance.id)
                                if doc_inst:
                                    doc_link_serializer = DockLinkTrimmedSerializer(doc_inst,data=doc_link_data, partial=True)
                                    if doc_link_serializer.is_valid(raise_exception=True):
                                        doc_link_serializer.save()

                            for theme_data in themes_data:
                                t_id = doc_link_data.pop('id')
                                t_inst = Theme.objects.get(id=t_id, practice=instance.id)
                                if t_inst:
                                    theme_serializer = ThemeTrimmedSerializer(t_inst,data=theme_data, partial=True)
                                    if theme_serializer.is_valid(raise_exception=True):
                                        theme_serializer.save()

                            if practice_serializer.is_valid(raise_exception=True):
                                practice_instance = practice_serializer.save()
                                

            elif isinstance(instance, CompanyRepresentativeProfile):
                company_rep_data = validated_data.pop('company_representative_profile', None)
                if company_rep_data:
                    company_rep_serializer = CompanyRepresentativeProfileSerializer(
                        instance.company_representative_profile, data=company_rep_data, partial=True
                    )
                    if company_rep_serializer.is_valid():
                        company_rep_serializer.save()

        return instances

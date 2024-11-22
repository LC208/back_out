# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    picture = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'faculty'
    
    def __str__(self):
        return self.name

class Speciality(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="specialities"
    )
    education_level = models.SmallIntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=512, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'base_speciality'

    def __str__(self):
        return self.code


class Companies(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    themes = models.CharField(max_length=255, blank=True, null=True)
    dbegin = models.CharField(max_length=255, blank=True, null=True)
    dend = models.CharField(max_length=255, blank=True, null=True)
    agreements = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    user = models.OneToOneField(User, models.DO_NOTHING, blank=True, null=True)
    area_of_activity = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name 

    class Meta:
        managed = False
        db_table = 'companies'

class CompanyRepresentativeProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_title = models.CharField(max_length=512, blank=True, null=True)
    user = models.OneToOneField(User, models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    messenger = models.CharField(max_length=128, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'models_collect_companyrepresentativeprofile'

class Practice(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(
        Companies, on_delete=models.DO_NOTHING, related_name="company"
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, related_name="faculty"
    )

    class Meta:
        managed = False
        db_table = 'base_practice'
    def __str__(self):
        return self.name 

class Theme(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    practice = models.ForeignKey(
        Practice, models.DO_NOTHING, blank=True, null=True, related_name="themes"
    )

    class Meta:
        managed = False
        db_table = 'base_theme'
    def __str__(self):
        return self.name 


class DocLink(models.Model):
    type = models.TextField()
    url = models.CharField(max_length=1000)
    practice = models.ForeignKey(
        Practice, on_delete=models.CASCADE, related_name="doc_links"
    )

    class Meta:
        managed = False
        db_table = 'base_doclink'
    def __str__(self):
        return self.name 


class DivisionsInst(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.ForeignKey('Faculty', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'divisions_inst'




class Groups(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_number = models.CharField(max_length=255, blank=True, null=True)
    stream = models.ForeignKey('Streams', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'




class Profiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profiles'


class Streams(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ForeignKey(Profiles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'streams'


class StudentOtchet(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True)
    link_ya = models.CharField(max_length=255, blank=True, null=True)
    status = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_otchet'


class StudentPractic(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)
    teacher = models.ForeignKey('TeacherScore', models.DO_NOTHING, blank=True, null=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    status = models.BigIntegerField(blank=True, null=True)
    company_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_practic'


class Students(models.Model):
    id = models.BigAutoField(primary_key=True)
    fio = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(Groups, models.DO_NOTHING, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    mira_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'


class TeacherScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    teacher = models.ForeignKey('Teachers', models.DO_NOTHING, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher_score'


class Teachers(models.Model):
    id = models.BigAutoField(primary_key=True)
    fio = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255, blank=True, null=True)
    work_load = models.BigIntegerField(blank=True, null=True)
    mira_id = models.BigIntegerField(blank=True, null=True)
    fac = models.ForeignKey(Faculty, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teachers'


class Templates(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Groups, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    decanat_check = models.BigIntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'templates'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    mira_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'users'

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthsUserprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    bitrix_user_id = models.IntegerField(blank=True, null=True)
    mira_id = models.IntegerField(blank=True, null=True)
    is_student = models.BooleanField()
    is_teacher = models.BooleanField()
    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'auths_userprofile'



class Faculty(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    picture = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'faculty'
    
    def __str__(self):
        return self.name

class Speciality(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="specialities"
    )

    class Meta:
        managed = False
        db_table = 'base_speciality'

    def __str__(self):
        return self.name


class Companies(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    themes = models.CharField(max_length=255, blank=True, null=True)
    dbegin = models.CharField(max_length=255, blank=True, null=True)
    dend = models.CharField(max_length=255, blank=True, null=True)
    agreements = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name 

    class Meta:
        managed = False
        db_table = 'companies'

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


class DjangoAdminLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.BigAutoField(primary_key=True)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'




class GroupScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    teacher_score = models.ForeignKey('TeacherScore', models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey('Groups', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_score'


class Groups(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_number = models.CharField(max_length=255, blank=True, null=True)
    stream = models.ForeignKey('Streams', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class Migrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    migration = models.CharField(max_length=255)
    batch = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


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

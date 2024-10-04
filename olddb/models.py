from django.db import models
from django.contrib.auth.models import User


class Companies(models.Model):
    name = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    # themes = models.CharField(max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)
    dbegin = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    dend = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    image = models.URLField(max_length=1000, null=True)
    agreements = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,related_name="company",null=True)
    class Meta:
        managed = True
        db_table = "companies"


class DivisionsInst(models.Model):
    name = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    faculty = models.ForeignKey("Faculty", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "divisions_inst"


class Faculty(models.Model):
    name = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    picture = models.URLField(max_length=1000)

    class Meta:
        managed = True
        db_table = "faculty"


class Groups(models.Model):
    group_number = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    stream = models.ForeignKey("Streams", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "groups"


class Profiles(models.Model):
    name = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "profiles"


class Streams(models.Model):
    name = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    full_name = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    code = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    year = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    profile = models.ForeignKey(Profiles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "streams"


class StudentOtchet(models.Model):
    student = models.ForeignKey("Students", models.DO_NOTHING, blank=True, null=True)
    link_ya = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "student_otchet"


class StudentPractic(models.Model):
    student = models.ForeignKey("Students", models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)
    teacher = models.ForeignKey("Teachers", models.DO_NOTHING, blank=True, null=True)
    theme = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    status = models.IntegerField(blank=True, null=True)
    company_path = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "student_practic"


class Students(models.Model):
    fio = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    group = models.ForeignKey(Groups, models.DO_NOTHING, blank=True, null=True)
    stud_id = models.IntegerField(blank=True, null=True)
    category = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "students"


class Teachers(models.Model):
    fio = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    post = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    work_load = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "teachers"


class Templates(models.Model):
    group = models.ForeignKey(Groups, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    decanat_check = models.IntegerField(blank=True, null=True)
    comment = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )
    date = models.CharField(
        max_length=255, db_collation="utf8mb3_general_ci", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "templates"

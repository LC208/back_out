from django.db import models
from olddb.models import Companies, Faculty


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

class Practice(models.Model):
    name = models.CharField(
        max_length=255, null=True
    )
    company = models.ForeignKey(
        Companies, on_delete=models.DO_NOTHING, related_name="company"
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, related_name="faculty"
    )

    def __str__(self) -> str:
        return self.name


class Theme(models.Model):
    name = models.CharField(
        max_length=255,  blank=True, null=True
    )
    practice = models.ForeignKey(
        Practice, models.DO_NOTHING, blank=True, null=True, related_name="themes"
    )

    def __str__(self):
        return self.name

class DocLink(models.Model):

    type = models.TextField()
    url = models.URLField(max_length=1000)
    practice = models.ForeignKey(
        Practice, on_delete=models.CASCADE, related_name="doc_links"
    )


class Speciality(models.Model):
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="specialities"
    )
    name = models.CharField(
        max_length=255,  blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name

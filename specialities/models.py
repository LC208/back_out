from django.db import models
from faculties.models import Faculty


class Speciality(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING, blank=True, null=True)
    education_level = models.IntegerField()

    class Meta:
        managed = False
        db_table = "university_speciality"

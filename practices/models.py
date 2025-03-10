from django.db import models

from companies.models import Companies
from faculties.models import Faculty
from doclinks.models import DocLink
from themes.models import Theme


class Practice(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(
        Companies, models.DO_NOTHING, blank=True, null=True, related_name="company"
    )
    faculty = models.ForeignKey(
        Faculty, models.DO_NOTHING, blank=True, null=True, related_name="faculty"
    )

    class Meta:
        managed = False
        db_table = "practice_practice"


class PracticeDocLinkRelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    contact = models.ForeignKey(DocLink, models.DO_NOTHING)
    practice = models.ForeignKey(Practice, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "practice_practicecontactrelation"
        unique_together = (("contact", "practice"),)


class PracticeThemeRelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    practice = models.ForeignKey(Practice, models.DO_NOTHING)
    theme = models.ForeignKey(Theme, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "practice_practicethemerelation"
        unique_together = (("theme", "practice"),)

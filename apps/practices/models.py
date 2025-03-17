from django.db import models

from apps.companies.models import Companies
from apps.faculties.models import Faculty
from apps.doclinks.models import DocLink
from apps.themes.models import Theme


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
    contact = models.ForeignKey(DocLink, models.CASCADE)
    practice = models.ForeignKey(Practice, models.CASCADE)

    class Meta:
        managed = False
        db_table = "practice_practicecontactrelation"
        unique_together = (("contact", "practice"),)


class PracticeThemeRelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    practice = models.ForeignKey(Practice, models.CASCADE)
    theme = models.ForeignKey(Theme, models.CASCADE)

    class Meta:
        managed = False
        db_table = "practice_practicethemerelation"
        unique_together = (("theme", "practice"),)

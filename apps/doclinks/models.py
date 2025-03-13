from django.db import models
from apps.companies.models import Companies


class DocLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.IntegerField()
    value = models.CharField(max_length=256)
    practices = models.ManyToManyField(
        "practices.Practice",
        through="practices.PracticeDocLinkRelation",
        related_name="doclinks",
    )
    company = models.ForeignKey(
        Companies, on_delete=models.SET_NULL, related_name="doclinks", null=True
    )

    class Meta:
        managed = False
        db_table = "practice_contact"

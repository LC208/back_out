from django.db import models
from companies.models import Companies


class DocLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.IntegerField()
    value = models.CharField(max_length=256)
    practices = models.ManyToManyField(
        "practices.Practice",
        through="practices.PracticeDocLinkRelation",
        related_name="doc_links",
    )
    company = models.ForeignKey(
        Companies, on_delete=models.DO_NOTHING, related_name="doc_links"
    )

    class Meta:
        managed = False
        db_table = "practice_contact"

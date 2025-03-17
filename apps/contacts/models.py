from django.db import models
from apps.companies.models import Companies


class Contact(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.IntegerField()
    value = models.CharField(max_length=256)
    practices = models.ManyToManyField(
        "practices.Practice",
        through="practices.PracticeContactRelation",
        related_name="contacts",
    )
    company = models.ForeignKey(
        Companies, on_delete=models.SET_NULL, related_name="contacts", null=True
    )

    class Meta:
        managed = False
        db_table = "practice_contact"

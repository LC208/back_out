from django.db import models


class Theme(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    practices = models.ManyToManyField(
        "practices.Practice",
        through="practices.PracticeThemeRelation",
        related_name="themes",
    )

    class Meta:
        managed = False
        db_table = "practice_theme"

from django.db import models
from apps.companies.models import Companies


class ThemeType(models.TextChoices):
    """
    Типы тем
    """

    THESIS = "ВКР", "Выпускная квалификационная работа"
    INDUSTRIAL = "ПР", "Производственная практика"
    RND = "НИОКР", "Научно-исследовательские и опытно-конструкторские работы"


class Theme(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    type = models.CharField(
        choices=ThemeType.choices,
        max_length=128,
        default=ThemeType.INDUSTRIAL,
        verbose_name="Тип практики",
    )
    practices = models.ManyToManyField(
        "practices.Practice",
        through="practices.PracticeThemeRelation",
        related_name="themes",
    )

    company = models.ForeignKey(
        Companies, on_delete=models.SET_NULL, related_name="themes", null=True
    )

    class Meta:
        managed = False
        db_table = "practice_theme"

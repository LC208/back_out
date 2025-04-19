from django.db import models
from apps.users.models import AuthsExtendedUser
from django.core.validators import MinValueValidator


class Companies(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    argeement_date_begin = models.DateField()
    agreement_date_end = models.DateField()
    agreement = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=1000, blank=True, null=True)
    area_of_activity = models.TextField(blank=True, null=True)
    head_full_name = models.CharField(max_length=128, blank=True, null=True)
    head_job_title = models.CharField(max_length=512, blank=True, null=True)
    user = models.OneToOneField(
        AuthsExtendedUser, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "practice_company"


class YearMetaCompany(models.Model):
    """
    Мета-информация по годам для компании
    """

    year = models.IntegerField(blank=False, null=False, verbose_name="Год")
    hire_count = models.IntegerField(
        default=1,
        verbose_name="Набор (кол-во студентов)",
        validators=(MinValueValidator(0),),
    )
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Компания",
        related_name="year_meta_company",
    )

    class Meta:
        managed = False
        db_table = "practice_yearmetacompany"
        verbose_name = "Мета-информация по годам для компании"
        verbose_name_plural = "Мета-информация по годам для компаний"
        constraints = [
            models.UniqueConstraint(
                fields=["year", "company"],
                name="unique_year_company_on_yearmetacompany",
            )
        ]

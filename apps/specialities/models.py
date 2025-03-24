from django.db import models
from apps.faculties.models import Faculty


class EducationLevel(models.IntegerChoices):
    """
    Степени образования
    """

    BACHELOR = 0, "Бакалавриат"
    SPECIALITY = 1, "Специалитет"
    MASTER = 2, "Магистратура"
    GRADUATE = 3, "Аспирантура"
    SPO = 4, "Среднее профессиональное образование"


class Speciality(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    faculty = models.ForeignKey(
        Faculty, models.DO_NOTHING, blank=True, null=True, related_name="specialities"
    )
    education_level = models.IntegerField(
        choices=EducationLevel.choices,
        default=EducationLevel.BACHELOR,
        verbose_name="Уровень образования",
    )
    ais_id = models.IntegerField(
        unique=True, blank=True, null=True, verbose_name="ID в АИС"
    )

    class Meta:
        managed = False
        db_table = "university_speciality"


class Stream(models.Model):
    """
    Поток
    """

    short_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Cоркащенное название потока",
    )
    full_name = models.CharField(
        max_length=255, blank=False, null=True, verbose_name="Полное название потока"
    )
    year = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Год поступления"
    )
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name="Спецаильность",
    )
    url = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Ссылка на направление обучения",
    )

    def __str__(self):
        if self.year:
            return f"{self.short_name}-{self.year}"
        return f"Поток {self.short_name}"

    class Meta:
        managed = False
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"
        db_table = "university_stream"

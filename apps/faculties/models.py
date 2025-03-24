from django.db import models


class Faculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=1000, blank=True, null=True)
    ais_id = models.IntegerField(
        unique=True, blank=True, null=True, verbose_name="ID в АИС"
    )

    def __str__(self):
        return self.name or f"Институт {self.id}"

    class Meta:
        managed = False
        db_table = "university_faculty"


class DirectionLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    short_name = models.CharField(max_length=255, blank=False, null=False)
    url = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "direction_link"

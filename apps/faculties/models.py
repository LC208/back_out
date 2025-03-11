from django.db import models


class Faculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name or f"Институт {self.id}"

    class Meta:
        managed = False
        db_table = "university_faculty"

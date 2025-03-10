from django.db import models
from users.models import AuthsExtendedUser


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

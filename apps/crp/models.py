from django.db import models
from apps.users.models import AuthsExtendedUser


class CompanyRepresentativeProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_title = models.CharField(max_length=512, blank=True, null=True)
    messenger = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=254)
    user = models.ForeignKey(
        AuthsExtendedUser, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "auths_companyrepresentativeprofile"

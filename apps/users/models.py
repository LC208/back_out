from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthsExtendedUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    patronymic = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "auths_extendeduser"

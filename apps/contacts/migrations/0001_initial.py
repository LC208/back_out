# Generated by Django 5.0.2 on 2025-03-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("type", models.IntegerField()),
                ("value", models.CharField(max_length=256)),
            ],
            options={
                "db_table": "practice_contact",
                "managed": False,
            },
        ),
    ]

# Generated by Django 5.0.2 on 2025-03-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Practice",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "practice_practice",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PracticeContactRelation",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "practice_practicecontactrelation",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PracticeThemeRelation",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "practice_practicethemerelation",
                "managed": False,
            },
        ),
    ]

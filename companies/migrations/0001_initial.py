# Generated by Django 5.0.2 on 2025-03-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('argeement_date_begin', models.DateField()),
                ('agreement_date_end', models.DateField()),
                ('agreement', models.CharField(blank=True, max_length=255, null=True)),
                ('image_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('area_of_activity', models.TextField(blank=True, null=True)),
                ('head_full_name', models.CharField(blank=True, max_length=128, null=True)),
                ('head_job_title', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'db_table': 'practice_company',
                'managed': False,
            },
        ),
    ]

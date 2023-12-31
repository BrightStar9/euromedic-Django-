# Generated by Django 2.2.6 on 2019-11-26 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0009_hospital_small_image")]

    operations = [
        migrations.AddField(
            model_name="location",
            name="municipality",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="location",
            name="municipality_en",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="location",
            name="municipality_sq",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="location",
            name="municipality_sr",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

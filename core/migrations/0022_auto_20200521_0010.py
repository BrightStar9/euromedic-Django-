# Generated by Django 2.2.4 on 2020-05-21 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0021_add_category_to_doctor")]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="specialization_details",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="specialization",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(name="Specialization"),
    ]

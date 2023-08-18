# Generated by Django 2.2.4 on 2020-05-11 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0020_add_image_to_doctor")]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="doctors",
                to="core.Category",
            ),
        ),
        migrations.AlterField(
            model_name="specialization",
            name="additional_info",
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
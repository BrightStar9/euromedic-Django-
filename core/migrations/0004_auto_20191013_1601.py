# Generated by Django 2.2.6 on 2019-10-13 16:01

import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0003_auto_20191008_2306")]

    operations = [
        migrations.AlterModelOptions(name="hospital", options={}),
        migrations.AlterField(
            model_name="category",
            name="icon",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="",
                validators=[core.validators.validate_image_and_svg_file_extension],
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="core.Category",
            ),
        ),
    ]
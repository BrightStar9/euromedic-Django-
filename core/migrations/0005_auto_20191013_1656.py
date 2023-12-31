# Generated by Django 2.2.6 on 2019-10-13 16:56

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0004_auto_20191013_1601")]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="icon",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="safesvg/",
                validators=[core.validators.validate_image_and_svg_file_extension],
            ),
        )
    ]

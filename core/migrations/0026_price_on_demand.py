# Generated by Django 2.2.4 on 2020-11-02 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0025_add_ordering_for_doctors")]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=None,
                max_digits=12,
                null=True,
                verbose_name="Standard price. Leave empty if price on demand",
            ),
        )
    ]

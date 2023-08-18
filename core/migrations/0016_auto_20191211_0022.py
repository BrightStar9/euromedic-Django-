# Generated by Django 2.2.6 on 2019-12-11 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0015_auto_20191203_2232")]

    operations = [
        migrations.AddField(
            model_name="service",
            name="description",
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="show_price_from",
            field=models.BooleanField(default=False),
        ),
    ]
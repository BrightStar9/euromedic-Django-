# Generated by Django 2.2.6 on 2019-12-16 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0016_auto_20191211_0022")]

    operations = [
        migrations.AddField(
            model_name="phonenumber",
            name="category",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="if a number is just for a specific category - select that category here. Otherwise - leave empty.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="phone_numbers",
                to="core.Category",
            ),
        )
    ]
# Generated by Django 2.2.4 on 2020-05-11 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0017_phonenumber_category")]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=200)),
                ("biography", models.TextField(max_length=1000)),
                (
                    "gender",
                    models.CharField(
                        choices=[("F", "Female"), ("M", "Male")], max_length=1
                    ),
                ),
                (
                    "hospitals",
                    models.ManyToManyField(
                        blank=True, related_name="doctors", to="core.Hospital"
                    ),
                ),
                (
                    "services",
                    models.ManyToManyField(
                        blank=True, related_name="doctors", to="core.Service"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Specialization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("additional_info", models.TextField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name="category",
            name="display_title",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name="Reference",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField(max_length=500)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctors",
                        to="core.Doctor",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="doctor",
            name="specialization",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="doctors",
                to="core.Specialization",
            ),
        ),
    ]

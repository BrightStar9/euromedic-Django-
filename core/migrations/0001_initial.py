# Generated by Django 2.2.6 on 2019-10-08 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("contenttypes", "0002_remove_content_type_name")]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                (
                    "slug",
                    models.CharField(
                        blank=True, db_index=True, max_length=100, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("name_sr", models.CharField(max_length=100, null=True)),
                ("name_en", models.CharField(max_length=100, null=True)),
                ("name_sq", models.CharField(max_length=100, null=True)),
                ("excerpt", models.TextField(blank=True, max_length=250, null=True)),
                ("excerpt_sr", models.TextField(blank=True, max_length=250, null=True)),
                ("excerpt_en", models.TextField(blank=True, max_length=250, null=True)),
                ("excerpt_sq", models.TextField(blank=True, max_length=250, null=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "description_sr",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "description_en",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "description_sq",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "image_mobile",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("icon", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.Category",
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Hospital",
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
                (
                    "slug",
                    models.CharField(
                        blank=True, db_index=True, max_length=100, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("name_sr", models.CharField(max_length=100, null=True)),
                ("name_en", models.CharField(max_length=100, null=True)),
                ("name_sq", models.CharField(max_length=100, null=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "description_sr",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "description_en",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "description_sq",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                ("hero_image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "transport_buses",
                    models.TextField(blank=True, max_length=250, null=True),
                ),
                (
                    "transport_trams",
                    models.TextField(blank=True, max_length=250, null=True),
                ),
                (
                    "transport_trolleys",
                    models.TextField(blank=True, max_length=250, null=True),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True, related_name="hospitals", to="core.Category"
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="HospitalType",
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
                ("name", models.CharField(max_length=100)),
                ("name_sr", models.CharField(max_length=100, null=True)),
                ("name_en", models.CharField(max_length=100, null=True)),
                ("name_sq", models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
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
                ("street", models.CharField(max_length=100)),
                ("number", models.CharField(max_length=20)),
                ("city", models.CharField(max_length=50)),
                ("city_sr", models.CharField(max_length=50, null=True)),
                ("city_en", models.CharField(max_length=50, null=True)),
                ("city_sq", models.CharField(max_length=50, null=True)),
                ("country", models.CharField(max_length=50)),
                ("country_sr", models.CharField(max_length=50, null=True)),
                ("country_en", models.CharField(max_length=50, null=True)),
                ("country_sq", models.CharField(max_length=50, null=True)),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True, decimal_places=10, max_digits=16, null=True
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True, decimal_places=10, max_digits=16, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkHours",
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
                ("workdays_start", models.TimeField()),
                ("workdays_end", models.TimeField()),
                ("saturday_start", models.TimeField(blank=True, null=True)),
                ("saturday_end", models.TimeField(blank=True, null=True)),
                ("sunday_start", models.TimeField(blank=True, null=True)),
                ("sunday_end", models.TimeField(blank=True, null=True)),
                (
                    "hospital",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="work_hours",
                        to="core.Hospital",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Service",
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
                (
                    "slug",
                    models.CharField(
                        blank=True, db_index=True, max_length=100, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("name_sr", models.CharField(max_length=200, null=True)),
                ("name_en", models.CharField(max_length=200, null=True)),
                ("name_sq", models.CharField(max_length=200, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                ("keywords", models.TextField(blank=True, max_length=1000, null=True)),
                (
                    "keywords_sr",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "keywords_en",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "keywords_sq",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="core.Category",
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="PhoneNumber",
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
                ("number", models.CharField(max_length=20)),
                (
                    "hospital",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="phone_numbers",
                        to="core.Hospital",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Image",
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
                ("img", models.ImageField(upload_to="")),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="hospital",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.Location",
            ),
        ),
        migrations.AddField(
            model_name="hospital",
            name="services",
            field=models.ManyToManyField(
                blank=True, related_name="hospitals", to="core.Service"
            ),
        ),
        migrations.AddField(
            model_name="hospital",
            name="types",
            field=models.ManyToManyField(
                related_name="hospitals", to="core.HospitalType"
            ),
        ),
    ]

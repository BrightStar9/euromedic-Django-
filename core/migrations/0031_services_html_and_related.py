# Generated by Django 2.2.4 on 2022-08-15 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_update_doctors_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='additional_info',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='related_services',
            field=models.ManyToManyField(blank=True, to='core.Service'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_en',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_sq',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_sr',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]

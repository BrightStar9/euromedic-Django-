# Generated by Django 2.2.4 on 2021-03-08 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_add_service_groups'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ['ordering_id']},
        ),
    ]
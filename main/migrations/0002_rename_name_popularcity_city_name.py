# Generated by Django 4.1.1 on 2022-09-19 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="popularcity",
            old_name="name",
            new_name="city_name",
        ),
    ]
